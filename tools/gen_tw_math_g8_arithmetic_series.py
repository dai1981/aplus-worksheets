# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：等差級數（108課綱 N-8-5）
  python3 tools/gen_tw_math_g8_arithmetic_series.py
1 ＋ 2 ＋ … ＋ n、Sₙ ＝ n（a₁ ＋ aₙ）÷ 2、首項・公差・項數から和、項數を先に求める和、奇數・倍數の和、生活の應用（座位・堆疊・存錢）。
誤答：÷ 2 を忘れる、項數を（末項 － 首項）÷ d にして ＋1 を忘れる、首項＋末項 を n 倍だけする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import sn, par, tidy_sets

R = random.Random(81015)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def S(a, d, n):
    return n * (2 * a + (n - 1) * d) // 2


def s1(seen):
    def mk():
        n = R.randint(10, 200)
        v = n * (n + 1) // 2
        q = "1 ＋ 2 ＋ 3 ＋ …… ＋ %d ＝ ？" % n
        return mcq(q, num(v), [num(n * (n + 1)), num(n * n // 2), num(n * (n - 1) // 2), num(v + n)], "首項 1、末項 %d、%d 項：%d ×（1 ＋ %d）÷ 2 ＝ %s。" % (n, n, n, n, num(v)))

    def fl():
        a, d, n = R.randint(-20, 30), nz(-6, 8), R.randint(8, 30)
        l = a + (n - 1) * d
        v = n * (a + l) // 2
        if n * (a + l) % 2:
            return None
        q = "等差級數的首項是 %s，末項是 %s，共 %d 項，總和是多少？" % (sn(a), sn(l), n)
        return mcq(q, sn(v), [sn(n * (a + l)), sn((a + l) // 2 if (a + l) % 2 == 0 else a + l), sn(v + l), sn((n - 1) * (a + l) // 2) if (n - 1) * (a + l) % 2 == 0 else sn(v - a)], "S ＝ %d ×（%s ＋ %s）÷ 2 ＝ %s。" % (n, sn(a), par(l), sn(v)))
    return pick_unique(R, mk, 8, seen) + pick_unique(R, fl, 12, seen)


def s2(seen):
    def mk():
        a, d, n = R.randint(-15, 30), nz(-5, 7), R.randint(6, 25)
        v = S(a, d, n)
        l = a + (n - 1) * d
        q = "首項 %s、公差 %s 的等差級數，前 %d 項的和是多少？" % (sn(a), sn(d), n)
        l2 = a + n * d
        return mcq(q, sn(v), [sn(n * (a + l2) // 2) if n * (a + l2) % 2 == 0 else sn(v + n), sn(n * (a + l)), sn(n * a + n * d), sn(v - l)],
                   "末項 %s ＋ %d × %s ＝ %s，S ＝ %d ×（%s ＋ %s）÷ 2 ＝ %s。" % (sn(a), n - 1, par(d), sn(l), n, sn(a), par(l), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, d, n = R.randint(-10, 20), nz(-6, 9), R.randint(8, 35)
        l = a + (n - 1) * d
        v = n * (a + l) // 2
        if n * (a + l) % 2:
            return None
        q = "%s ＋ %s ＋ %s ＋ …… ＋ %s ＝ ？" % (sn(a), par(a + d), par(a + 2 * d), par(l))
        n2 = (l - a) // d
        return mcq(q, sn(v), [sn(n2 * (a + l) // 2) if n2 * (a + l) % 2 == 0 else sn(v - l), sn(n * (a + l)), sn((n + 1) * (a + l) // 2) if (n + 1) * (a + l) % 2 == 0 else sn(v + l), sn(a + l)],
                   "公差 %s，項數 ＝（%s － %s）÷ %s ＋ 1 ＝ %d，和 ＝ %d ×（%s ＋ %s）÷ 2 ＝ %s。" % (sn(d), sn(l), par(a), par(d), n, n, sn(a), par(l), sn(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def odd():
        n = R.randint(5, 60)
        l = 2 * n - 1
        q = "1 ＋ 3 ＋ 5 ＋ …… ＋ %d ＝ ？" % l
        return mcq(q, num(n * n), [num(l * (l + 1) // 2), num((n - 1) ** 2), num(n * l), num(n * (n + 1))], "共（%d － 1）÷ 2 ＋ 1 ＝ %d 項，和 ＝ %d ×（1 ＋ %d）÷ 2 ＝ %s。" % (l, n, n, l, num(n * n)))

    def mult():
        k = R.choice([3, 4, 5, 6, 7, 8, 9, 11, 12])
        top = R.choice([50, 100, 150, 200])
        n = top // k
        l = n * k
        v = k * n * (n + 1) // 2
        q = "1 到 %d 之間所有 %d 的倍數，總和是多少？" % (top, k)
        return mcq(q, num(v), [num(k * (n - 1) * n // 2), num(n * (k + l)), num(top * (top + 1) // 2 // k), num(v + l)], "%d，%d，……，%d 共 %d 項，和 ＝ %d ×（%d ＋ %d）÷ 2 ＝ %s。" % (k, 2 * k, l, n, n, k, l, num(v)))
    return pick_unique(R, odd, 8, seen) + pick_unique(R, mult, 12, seen)


def s5(seen):
    def seats():
        a, d, n = R.randint(15, 30), R.choice([1, 2, 2, 3]), R.randint(10, 25)
        v = S(a, d, n)
        q = "禮堂第 1 排有 %d 個座位，之後每排比前一排多 %d 個，共 %d 排。禮堂一共有幾個座位？" % (a, d, n)
        l = a + (n - 1) * d
        return mcq(q, "%s 個" % num(v), ["%s 個" % num(x) for x in (n * (a + l), l * n, a * n, v + l)], "最後一排 %d ＋ %d × %d ＝ %d，%d ×（%d ＋ %d）÷ 2 ＝ %s（個）。" % (a, n - 1, d, l, n, a, l, num(v)))

    def pile():
        top, n = R.randint(1, 6), R.randint(5, 14)
        bot = top + n - 1
        v = n * (top + bot) // 2
        if n * (top + bot) % 2:
            return None
        q = "一堆鋼管，最上層 %d 根，往下每層多 1 根，最下層 %d 根。一共有幾根？" % (top, bot)
        return mcq(q, "%d 根" % v, ["%d 根" % x for x in (n * (top + bot), bot * (bot + 1) // 2 if top > 1 else v + bot, (bot - top) * (top + bot) // 2, v - bot)], "共 %d － %d ＋ 1 ＝ %d 層，%d ×（%d ＋ %d）÷ 2 ＝ %d（根）。" % (bot, top, n, n, top, bot, v))

    def save():
        who = NM.next()
        a, d = R.choice([10, 20, 50]), R.choice([5, 10, 20])
        n = R.randint(8, 20)
        v = S(a, d, n)
        q = "%s第 1 天存 %d 元，以後每天比前一天多存 %d 元。%d 天一共存了多少元？" % (who, a, d, n)
        l = a + (n - 1) * d
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (n * (a + l), l, n * l, S(a, d, n - 1))], "第 %d 天存 %d 元，%d ×（%d ＋ %d）÷ 2 ＝ %s（元）。" % (n, l, n, a, l, num(v)))
    return pick_unique(R, seats, 7, seen) + pick_unique(R, pile, 6, seen) + pick_unique(R, save, 7, seen)


def main():
    seen = set()
    sets = [("首項加末項", s1(seen)), ("用首項、公差求和", s2(seen)), ("先求項數再求和", s3(seen)),
            ("奇數與倍數的和", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["把等差數列的每一項加起來叫<b>等差級數</b>。",
         "<b>和 ＝ 項數 ×（首項 ＋ 末項）÷ 2</b>：把數列倒過來排，上下兩兩相加都一樣大。",
         "不知道末項時，先算末項 ＝ 首項 ＋（n － 1）× 公差；不知道項數時，項數 ＝（末項 － 首項）÷ 公差 ＋ 1。"],
        [example("1 ＋ 2 ＋ …… ＋ 100", ["100 項，首項 1，末項 100。", "100 ×（1 ＋ 100）÷ 2。"], "5050"),
         example("5 ＋ 8 ＋ 11 ＋ …… ＋ 62", ["項數（62 － 5）÷ 3 ＋ 1 ＝ 20。", "20 ×（5 ＋ 62）÷ 2 ＝ 670。"], "670")],
        [("忘了 ÷ 2", "（首項 ＋ 末項）× 項數 是兩倍的和"),
         ("項數 ＝（62 － 5）÷ 3 ＝ 19", "要再 ＋ 1，共 20 項"),
         ("用公差當末項", "末項要先算出來")])
    faq = [{"q": "等差級數公式為什麼要除以 2？",
            "a": "把數列正著寫一次、倒著寫一次，上下相加每一組都是首項 ＋ 末項，共有項數組，這是兩倍的和，所以要除以 2。"},
           {"q": "1 加到 100 為什麼是 5050？",
            "a": "1 ＋ 100、2 ＋ 99、…… 每組都是 101，共 50 組：101 × 50 ＝ 5050。"},
           {"q": "八年級的等差級數要學什麼？",
            "a": "108課綱 N-8-5：等差級數求和公式，以及在生活中的應用。"}]
    make_unit(R, "grade-8", "arithmetic-series", "N-8-5",
              "等差級數求和：等差級數求和公式；生活中的應用。",
              "等差級數求和",
              "八年級數學 等差級數 練習題｜求和公式・項數・應用題 學習單（附解答）",
              "等差級數",
              "國中八年級數學「等差級數求和」免費學習單：首項加末項的求和公式、用首項和公差求和、先求項數再求和、奇數與倍數的和、座位與存錢應用題。100題線上練習馬上對答案，附可列印解答。",
              "和 ＝ 項數 ×（首項 ＋ 末項）÷ 2",
              "項數 ＝（末項 － 首項）÷ 公差 ＋ 1。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
