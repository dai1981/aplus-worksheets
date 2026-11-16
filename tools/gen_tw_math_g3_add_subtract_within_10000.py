# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：10000以內的加減（108課綱 N-3-2）
  python3 tools/gen_tw_math_g3_add_subtract_within_10000.py
三、四位數的加減直式（多次進位、退位、連續退位、跨0退位）與應用問題。
誤答は「進位を忘れる」「大きい数から小さい数を引いてしまう」「退位を2回してしまう」など、よくある間違いから作る。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(31002)


def no_carry_add(a, b):
    """進位を忘れる：各位の和の一の位だけを書く"""
    s, p = 0, 1
    while a or b:
        s += ((a % 10 + b % 10) % 10) * p
        a //= 10; b //= 10; p *= 10
    return s


def no_borrow_sub(a, b):
    """退位しないで、各位の大きい方から小さい方を引く"""
    s, p = 0, 1
    while a or b:
        s += abs(a % 10 - b % 10) * p
        a //= 10; b //= 10; p *= 10
    return s


def carries(a, b):
    c = n = 0
    while a or b:
        c = 1 if a % 10 + b % 10 + c >= 10 else 0
        n += c
        a //= 10; b //= 10
    return n


def borrows(a, b):
    c = n = 0
    while a or b:
        d = a % 10 - c - b % 10
        c = 1 if d < 0 else 0
        n += c
        a //= 10; b //= 10
    return n


def add_q(lo, hi, lo2, hi2, need=1):
    def mk():
        a, b = R.randint(lo, hi), R.randint(lo2, hi2)
        if a + b > 9999 or carries(a, b) < need:
            return None
        s = a + b
        w = [no_carry_add(a, b), s + 10, s - 10, s + 100, s - 100, s + 1000]
        return mcq("%s ＋ %s ＝" % (a, b), num(s), [num(x) for x in w if x != s and x > 0],
                   "直式由個位開始加，滿10要進位到左邊一位：%s ＋ %s ＝ %s。" % (a, b, num(s)))
    return mk


def sub_q(lo, hi, lo2, hi2, need=1, zero=False):
    def mk():
        a, b = R.randint(lo, hi), R.randint(lo2, hi2)
        if zero:   # 5003、6040 のように 0 が続く数（跨0退位）
            a = R.randint(2, 9) * 1000 + R.choice([R.randint(1, 9), R.randint(1, 9) * 10])
        if b >= a or borrows(a, b) < need:
            return None
        d = a - b
        w = [no_borrow_sub(a, b), d + 10, d - 10, d + 100, d - 100, d + 1000]
        return mcq("%s － %s ＝" % (a, b), num(d), [num(x) for x in w if x != d and x > 0],
                   "個位不夠減，要向十位借1當10（退位）。%s － %s ＝ %s，可以用 %s ＋ %s ＝ %s 驗算。"
                   % (a, b, num(d), num(d), b, a))
    return mk


def s5(seen):
    nm = Names(R)

    def a():
        who = nm.next()
        have, spend = R.randint(1500, 9000), R.randint(300, 2900)
        if spend >= have or borrows(have, spend) < 1:
            return None
        mw, thing = R.choice([("個", "書包"), ("頂", "腳踏車安全帽"), ("套", "故事書"), ("雙", "運動鞋"), ("台", "電子辭典")])
        r = have - spend
        q = "%s有 %s 元，買了一%s %s 元的%s，還剩下多少元？" % (who, num(have), mw, num(spend), thing)
        return mcq(q, "%s元" % num(r), ["%s元" % num(x) for x in (have + spend, no_borrow_sub(have, spend), r + 100, r - 10) if x != r and x > 0],
                   "剩下的錢用減法：%s － %s ＝ %s（元）。" % (num(have), num(spend), num(r)))

    def b():
        x, y = R.randint(1200, 5000), R.randint(800, 4000)
        if x + y > 9999 or carries(x, y) < 2:
            return None
        place = R.choice(["圖書館上午借出", "動物園上午有", "博物館星期六有"])
        q2 = {"圖書館上午借出": ("本書，下午借出", "本，這一天一共借出幾本？", "本"),
              "動物園上午有": ("位遊客，下午有", "位，這一天一共有幾位遊客？", "位"),
              "博物館星期六有": ("人參觀，星期日有", "人，兩天一共有幾人？", "人")}[place]
        s = x + y
        q = "%s %s %s %s %s" % (place, num(x), q2[0], num(y), q2[1])
        return mcq(q, num(s) + q2[2], [num(v) + q2[2] for v in (no_carry_add(x, y), abs(x - y), s + 100, s - 1000) if v != s and v > 0],
                   "合起來用加法：%s ＋ %s ＝ %s。" % (num(x), num(y), num(s)))

    def c():
        x, y = R.randint(2000, 9000), R.randint(500, 4000)
        if y >= x or borrows(x, y) < 1:
            return None
        q = "學校運動會要準備 %s 瓶水，已經買了 %s 瓶，還差幾瓶？" % (num(x), num(y))
        r = x - y
        return mcq(q, "%s瓶" % num(r), ["%s瓶" % num(v) for v in (x + y, no_borrow_sub(x, y), r + 10, r - 100) if v != r and v > 0],
                   "還差的數量用減法：%s － %s ＝ %s（瓶）。" % (num(x), num(y), num(r)))

    def d():
        a1 = R.randint(1000, 4000)
        more = R.randint(200, 1500)
        b1 = a1 + more
        if carries(a1, more) < 1:
            return None
        who1, who2 = nm.next(), nm.next()
        q = "%s的存錢筒有 %s 元，%s比%s多 %s 元，%s有多少元？" % (who1, num(a1), who2, who1, num(more), who2)
        return mcq(q, "%s元" % num(b1), ["%s元" % num(v) for v in (a1 - more, no_carry_add(a1, more), b1 + 100, more) if v != b1 and v > 0],
                   "比 %s 多 %s，用加法：%s ＋ %s ＝ %s（元）。" % (num(a1), num(more), num(a1), num(more), num(b1)))
    return pick_unique(R, a, 5, seen) + pick_unique(R, b, 5, seen) + pick_unique(R, c, 5, seen) + pick_unique(R, d, 5, seen)


def main():
    seen = set()
    sets = [
        ("三位數加法（進位）", pick_unique(R, add_q(120, 899, 110, 899, 1), 20, seen)),
        ("四位數加法（多次進位）", pick_unique(R, add_q(1000, 7999, 150, 4999, 2), 20, seen)),
        ("減法（退位）", pick_unique(R, sub_q(300, 9999, 100, 4999, 1), 20, seen)),
        ("連續退位和跨0退位", pick_unique(R, sub_q(0, 0, 100, 1999, 2, zero=True), 10, seen)
                             + pick_unique(R, sub_q(1000, 9999, 199, 5999, 3), 10, seen)),
        ("應用問題", s5(seen)),
    ]
    body = lesson(
        ["直式要把<b>個位對齊個位</b>，從個位開始算。",
         "加法：同一位加起來<b>滿10，就進1</b>到左邊一位。",
         "減法：不夠減時，向左邊一位<b>借1當10</b>（退位）。左邊是0時，要再往左借。",
         "算完用相反的算法<b>驗算</b>：減法的答案 ＋ 減數 ＝ 被減數。"],
        [example("2768 ＋ 1574 ＝", ["個位 8＋4＝12，寫2進1。十位 6＋7＋1＝14，寫4進1。",
                                     "百位 7＋5＋1＝13，寫3進1。千位 2＋1＋1＝4。"], "4342"),
         example("5003 － 1268 ＝", ["個位 3 不夠減8。十位、百位都是0，要從千位借。",
                                     "5003 看成 4個千、9個百、9個十、13個一。", "13－8＝5，9－6＝3，9－2＝7，4－1＝3。"], "3735")],
        [("進位的1忘了加", "直式上方寫小小的1，加那一位時一起加"),
         ("個位 3－8 不夠減，就改算 8－3", "要先向十位借1當10，算 13－8"),
         ("5003－1268，從0借不了就跳過", "0要先向左邊借，變成9，再借給右邊")])
    faq = [{"q": "三年級的加減直式要學到幾位數？",
            "a": "108課綱 N-3-2 要會10000以內的加減直式，包括多次進位和退位，例如 2768＋1574、5003－1268。"},
           {"q": "退位減法一直算錯怎麼辦？",
            "a": "先在直式上寫出借位後的數字（例如 5003 寫成 4、9、9、13），再一位一位減，最後用加法驗算。"},
           {"q": "有沒有可以列印的加減直式學習單？",
            "a": "有。本頁的100題可以線上作答，也可以免費列印A4學習單，最後一頁是解答。"}]
    make_unit(R, "grade-3", "add-subtract-within-10000", "N-3-2", "加減直式計算：含加、減法多次進、退位。",
              "10000以內的加減：直式進位與退位",
              "三年級數學 加減直式 練習題｜進位・退位・跨0退位 學習單（附解答）",
              "10000以內的加減",
              "國小三年級數學「10000以內的加減」免費學習單：三、四位數加減直式，多次進位、連續退位、跨0退位和應用題。100題線上練習馬上對答案，附可列印解答。",
              "個位對齊，從個位算起：滿10進1，不夠借1當10",
              "減法算完用加法驗算：答案 ＋ 減數 ＝ 被減數。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
