# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：小數的除法（108課綱 N-6-4）
  python3 tools/gen_tw_math_g6_dividing_decimals.py
整數÷小數・小數÷小數：除數を整數にするため被除數と除數の小數點を同じ桁だけ右へ移す。直式、商と被除數の大小、應用。
誤答：除數だけ小數點を動かす、移す桁數を被除數と除數で違える、「商は必ず被除數より小さい」と思う。
"""
import random
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num

R = random.Random(61004)
NM = Names(R)


def s(x):
    x = D(x)
    if x.as_tuple().exponent < -3:
        x = x.quantize(D("0.01"))
    x = x.normalize()
    t = format(x, "f")
    if "." in t:
        i, f = t.split(".")
        return num(int(i)) + "." + f
    return num(int(t))


def pair(dp_div, int_dvd=False):
    """除數（小數 dp_div 位）・商 → 被除數"""
    while True:
        dv = D(R.randint(2, 99 if dp_div == 1 else 99)) / (10 ** dp_div)
        if dv >= 10 or dv == dv.to_integral_value():
            continue
        qt = D(R.randint(2, 60)) if int_dvd else D(R.randint(12, 480)) / 10
        dd = dv * qt
        if int_dvd and dd != dd.to_integral_value():
            continue
        if not int_dvd and dd == dd.to_integral_value():
            continue
        if dd.as_tuple().exponent < -3:
            continue
        return dd, dv, qt


def wrongs(dd, dv, qt):
    return [s(qt * 10), s(qt / 10), s(qt * 100) if qt * 100 < 100000 else s(qt + 1), s(qt + D("0.1") if qt != qt.to_integral_value() else qt + 1)]


def s1(seen):
    def mk():
        dd, dv, qt = pair(R.choice([1, 2]), True)
        k = -dv.as_tuple().exponent
        q = "%s ÷ %s ＝" % (s(dd), s(dv))
        e = "除數 %s 有 %d 位小數，被除數和除數都乘以 %d：%s ÷ %s ＝ %s。" % (s(dv), k, 10 ** k, s(dd * 10 ** k), s(dv * 10 ** k), s(qt))
        return mcq(q, s(qt), wrongs(dd, dv, qt), e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        dd, dv, qt = pair(1, False)
        q = "%s ÷ %s ＝" % (s(dd), s(dv))
        e = "被除數和除數的小數點同時往右移 1 位：%s ÷ %s ＝ %s。" % (s(dd * 10), s(dv * 10), s(qt))
        return mcq(q, s(qt), wrongs(dd, dv, qt), e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def shift():
        dd, dv, qt = pair(R.choice([1, 2]), R.random() < .5)
        k = -dv.as_tuple().exponent
        q = "用直式算 %s ÷ %s，先把它改成哪一個算式？" % (s(dd), s(dv))
        ans = "%s ÷ %s" % (s(dd * 10 ** k), s(dv * 10 ** k))
        w = ["%s ÷ %s" % (s(dd), s(dv * 10 ** k)), "%s ÷ %s" % (s(dd * 10 ** (k + 1)), s(dv * 10 ** k)), "%s ÷ %s" % (s(dd * 10 ** k), s(dv))]
        return mcq(q, ans, w, "除數變成整數要乘以 %d，被除數也要乘以 %d，商不變：%s。" % (10 ** k, 10 ** k, ans))

    def same():
        dd, dv, qt = pair(1, R.random() < .5)
        k = R.choice([10, 100])
        q = "%s ÷ %s 的商，和下面哪一個算式的商一樣？" % (s(dd), s(dv))
        ans = "%s ÷ %s" % (s(dd * k), s(dv * k))
        return mcq(q, ans, ["%s ÷ %s" % (s(dd * k), s(dv)), "%s ÷ %s" % (s(dd), s(dv * k)), "%s ÷ %s" % (s(dd * k), s(dv * k * 10))],
                   "被除數和除數同時乘以同一個數，商不變。")
    return pick_unique(R, shift, 12, seen) + pick_unique(R, same, 8, seen)


def s4(seen):
    def mk():
        a = D(R.randint(12, 900)) / R.choice([1, 10])
        dv = D(R.randint(1, 30)) / 10
        if dv == 1 or dv == dv.to_integral_value():
            return None
        big = dv < 1
        q = "不用算出答案：%s ÷ %s 的商，比 %s 大還是小？" % (s(a), s(dv), s(a))
        ans = "比 %s 大" % s(a) if big else "比 %s 小" % s(a)
        return mcq(q, ans, ["比 %s 小" % s(a) if big else "比 %s 大" % s(a), "和 %s 一樣" % s(a), "不一定"],
                   ("除數 %s 比 1 小，所以商比被除數大。除以比 1 小的數，商會變大。" if big else "除數 %s 比 1 大，所以商比被除數小。") % s(dv))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def rope():
        L = D(R.randint(30, 150)) / 10
        p = D(R.choice([3, 4, 5, 6, 8, 12, 15, 25])) / 10
        n = int(L / p)
        if n < 2 or L % p == 0:
            return None
        rem = L - p * n
        q = "一條 %s 公尺的繩子，每 %s 公尺剪一段，最多可以剪成幾段？剩下幾公尺？" % (s(L), s(p))
        ans = "%d 段，剩 %s 公尺" % (n, s(rem))
        return mcq(q, ans, ["%d 段，剩 %s 公尺" % (n, s(rem * 10)), "%d 段，剩 %s 公尺" % (n + 1, s(rem)), "%d 段，剩 %s 公尺" % (n - 1, s(rem + p))],
                   "%s ÷ %s ＝ %d……%s。餘數的小數點要對齊原來的被除數，是 %s 公尺，不是 %s。" % (s(L), s(p), n, s(rem), s(rem), s(rem * 10)))

    def price():
        kg = D(R.randint(5, 35)) / 10
        unit = R.choice([40, 60, 80, 120, 150, 180, 240])
        tot = kg * unit
        if tot != tot.to_integral_value():
            return None
        item = R.choice(["香蕉", "芭樂", "白米", "地瓜"])
        q = "買 %s 公斤%s付了 %s 元。1 公斤多少元？" % (s(kg), item, s(tot))
        return mcq(q, "%d 元" % unit, ["%s 元" % x for x in (s(tot * kg), s(D(unit) / 10), s(D(unit) * 10))], "%s ÷ %s ＝ %d（元）。" % (s(tot), s(kg), unit))

    def times():
        a = D(R.randint(12, 90)) / 10
        k = D(R.choice([5, 15, 25, 12, 4, 8])) / 10
        b = a * k
        if b.as_tuple().exponent < -2:
            return None
        who = NM.next()
        q = "%s的身高是 %s 公尺，影子長 %s 公尺。影子是身高的幾倍？" % (who, s(a), s(b)) if False else \
            "哥哥存了 %s 萬元，是弟弟的 %s 倍。弟弟存了多少萬元？" % (s(b), s(k))
        return mcq(q, "%s 萬元" % s(a), ["%s 萬元" % x for x in (s(b * k), s(a * 10), s(a / 10))], "弟弟 × %s ＝ %s，弟弟 ＝ %s ÷ %s ＝ %s（萬元）。" % (s(k), s(b), s(b), s(k), s(a)))
    return pick_unique(R, rope, 7, seen) + pick_unique(R, price, 7, seen) + pick_unique(R, times, 6, seen)


def main():
    seen = set()
    sets = [("整數除以小數", s1(seen)), ("小數除以小數", s2(seen)), ("直式：移動小數點", s3(seen)),
            ("商比被除數大還是小", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["除數是小數時，把<b>除數和被除數的小數點同時往右移</b>同樣的位數，讓除數變成整數，商不變。",
         "例如 7.2 ÷ 0.3 ＝ 72 ÷ 3 ＝ 24。",
         "除以比 1 小的數，商會比被除數大；除以比 1 大的數，商會比被除數小。",
         "有餘數時，餘數的小數點要對齊<b>原來</b>被除數的小數點。"],
        [example("4.56 ÷ 0.12", ["小數點都往右移 2 位：456 ÷ 12。"], "38"),
         example("6.5 ÷ 0.4 ＝ ？……？（商是整數）", ["65 ÷ 4 ＝ 16……1。", "餘數對齊原來的小數點：0.1。"], "16……0.1")],
        [("只移除數的小數點", "被除數也要移同樣的位數"),
         ("餘數寫成 1", "要對齊原來的小數點：0.1"),
         ("以為除完一定變小", "除以 0.5，答案是原來的 2 倍")])
    faq = [{"q": "小數除以小數怎麼算？",
            "a": "把除數變成整數：除數和被除數的小數點同時往右移同樣位數，再照整數除法算，商的小數點對齊移動後的被除數。"},
           {"q": "為什麼可以同時移動小數點？",
            "a": "被除數和除數同時乘以 10 或 100，商不變。例如 7.2 ÷ 0.3 和 72 ÷ 3 的答案都是 24。"},
           {"q": "六年級的小數除法要學什麼？",
            "a": "108課綱 N-6-4：整數除以小數、小數除以小數的意義和直式計算，並處理「商一定比被除數小」的錯誤想法。"}]
    make_unit(R, "grade-6", "dividing-decimals", "N-6-4",
              "小數的除法：整數除以小數、小數除以小數的意義。直式計算。教師用位值的概念說明直式計算的合理性。處理商一定比被除數小的錯誤類型。",
              "小數的除法：除數是小數",
              "六年級數學 小數除法 練習題｜整數除以小數・小數除以小數・直式 學習單（附解答）",
              "小數的除法",
              "國小六年級數學「小數的除法」免費學習單：整數除以小數、小數除以小數、直式移動小數點、商和被除數的大小、餘數的小數點與應用題。100題線上練習馬上對答案，附可列印解答。",
              "除數和被除數的小數點同時往右移",
              "除數變成整數，商不變。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
