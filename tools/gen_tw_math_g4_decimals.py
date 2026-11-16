# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：二位小數（108課綱 N-4-7）
  python3 tools/gen_tw_math_g4_decimals.py
百分位、幾個0.01、比大小、直式加減（小數點對齊）、整數倍、單位換算（公尺・公分、元）、應用問題。
誤答：桁数で大小を決める（0.8 < 0.65）、小數點を右揃えにする、0.01 と 0.1 の取り違え、繰り上がり忘れ。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, dnum, fr

R = random.Random(41008)
NM = Names(R)


def D(h):
    """h 個の 0.01 → 小數（235 → 2.35、230 → 2.3）"""
    return dnum(h / 100, 2)


def s1(seen):
    def place():
        h = R.randint(101, 999)
        if h % 10 == 0 or len(set(str(h))) < 3:
            return None
        k = R.choice(["個位", "十分位", "百分位"])
        s = str(h)
        dg = {"個位": s[0], "十分位": s[1], "百分位": s[2]}
        return mcq("%s 的<b>%s</b>數字是多少？" % (D(h), k), dg[k], [v for kk, v in dg.items() if kk != k] + [str((int(dg[k]) + 1) % 10), str((int(dg[k]) + 2) % 10)],
                   "%s：個位 %s，十分位 %s，百分位 %s。" % (D(h), s[0], s[1], s[2]))

    def count():
        h = R.randint(11, 999)
        if h % 10 == 0:
            return None
        if R.random() < .5:
            return mcq("%s 是幾個 0.01？" % D(h), "%d 個" % h, ["%d 個" % x for x in (h // 10, h * 10, int(D(h).replace(".", "").lstrip("0") or 0) + 1, h + 100)],
                       "1 是 100 個 0.01，%s 是 %d 個 0.01。" % (D(h), h))
        return mcq("%d 個 0.01 是多少？" % h, D(h), [D(h * 10) if h < 100 else D(h // 10 * 10 + 1), dnum(h / 1000, 3), str(h), D(h + 100)],
                   "100 個 0.01 是 1，%d 個 0.01 是 %s。" % (h, D(h)))

    def frac():
        h = R.randint(1, 99)
        if h % 10 == 0:
            return None
        return mcq("%s 寫成小數是多少？" % fr(h, 100), D(h), [dnum(h / 10, 1), dnum(h / 1000, 3), str(h)], "%s 是 %d 個 0.01，就是 %s。" % (fr(h, 100), h, D(h)))
    return pick_unique(R, place, 7, seen) + pick_unique(R, count, 8, seen) + pick_unique(R, frac, 5, seen)


def s2(seen):
    def cmp_():
        a = R.randint(1, 99) * 10 if R.random() < .4 else R.randint(1, 999)
        b = R.randint(1, 999)
        if a == b or a % 100 == 0 or b % 100 == 0:
            return None
        sign = ">" if a > b else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % (D(a), D(b)), sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "從個位開始一位一位比：%s %s %s。%s" % (D(a), sign, D(b), "（%s ＝ %.2f）" % (D(a), a / 100) if a % 10 == 0 else ""))

    def big():
        hs = R.sample(range(5, 400), 4)
        if len({h // 10 for h in hs}) < 4 or any(h % 100 == 0 for h in hs):
            return None
        ask = R.choice(["最大", "最小"])
        t = max(hs) if ask == "最大" else min(hs)
        labs = [D(h) for h in hs]
        return mcq("%s 中，哪一個%s？" % ("、".join(labs), ask), D(t), [l for l in labs if l != D(t)], "小數比大小不是看位數多少，要從個位、十分位、百分位依序比：%s的是 %s。" % (ask, D(t)))
    return pick_unique(R, cmp_, 12, seen) + pick_unique(R, big, 8, seen)


def s3(seen):
    def add():
        a, b = R.randint(105, 899), R.randint(15, 699)
        if a % 10 == 0 or (R.random() < .3 and b >= 100):
            b = R.randint(1, 9) * 10 + (0 if R.random() < .5 else 0)
        s = a + b
        w = [D(a + b * 10) if b < 100 else D(s + 100), D(s + 10), D(s - 10), D(s + 1), D(s + 100)]
        return mcq("%s ＋ %s ＝" % (D(a), D(b)), D(s), [x for x in w if x != D(s)],
                   "小數點對齊，從百分位加起，滿 10 進位：%s。" % D(s))

    def sub():
        a = R.randint(300, 999)
        b = R.randint(15, a - 50)
        if b % 10 == 0 and R.random() < .5:
            return None
        d = a - b
        w = [D(d + 10), D(d - 10), D(d + 1), D(abs(a - b * 10)) if b * 10 < a else D(d + 100), D(d - 100) if d > 100 else D(d + 20)]
        return mcq("%s － %s ＝" % (D(a), D(b)), D(d), [x for x in w if x != D(d)],
                   "小數點對齊，不夠減向前一位借 1：%s。" % D(d))
    return pick_unique(R, add, 10, seen) + pick_unique(R, sub, 10, seen)


def s4(seen):
    def times():
        a = R.randint(12, 399)
        k = R.randint(2, 9)
        if a % 10 == 0:
            return None
        v = a * k
        return mcq("%s × %d ＝" % (D(a), k), D(v), [D(v * 10), D(v // 10) if v // 10 else D(v + 1), D(v + a), str(v)],
                   "%s 是 %d 個 0.01，× %d 是 %d 個 0.01，就是 %s。" % (D(a), a, k, v, D(v)))

    def unit():
        kind = R.choice(["m", "yuan", "kg"])
        h = R.randint(101, 999)
        if h % 100 == 0:
            return None
        if kind == "m":
            return mcq("%d 公分是幾公尺？" % h, D(h) + " 公尺", [dnum(h / 10, 1) + " 公尺", dnum(h / 1000, 3) + " 公尺", str(h) + " 公尺"],
                       "1 公分 ＝ 0.01 公尺，%d 公分 ＝ %s 公尺。" % (h, D(h)))
        if kind == "kg":
            g = h * 10
            return mcq("%d 公克是幾公斤？" % g, D(h) + " 公斤", [dnum(g / 100, 1) + " 公斤", dnum(g / 100000, 4) + " 公斤", str(g) + " 公斤"],
                       "1000 公克 ＝ 1 公斤，10 公克 ＝ 0.01 公斤，%d 公克 ＝ %s 公斤。" % (g, D(h)))
        return mcq("%s 公尺是幾公分？" % D(h), "%d 公分" % h, ["%s 公分" % x for x in (dnum(h / 10, 1), str(h * 10), D(h))],
                   "1 公尺 ＝ 100 公分，%s 公尺 ＝ %d 公分。" % (D(h), h))
    return pick_unique(R, times, 10, seen) + pick_unique(R, unit, 10, seen)


def s5(seen):
    def jump():
        a, b = R.randint(250, 420), R.randint(5, 60)
        if a % 10 == 0:
            return None
        who, o = NM.next(), NM.next()
        if who == o:
            return None
        q = "%s跳遠跳了 %s 公尺，比%s多 %s 公尺。%s跳了幾公尺？" % (who, D(a), o, D(b), o)
        d = a - b
        return mcq(q, D(d) + " 公尺", [D(a + b) + " 公尺", D(d + 10) + " 公尺", D(abs(a - b * 10)) + " 公尺" if b * 10 < a else D(d - 1) + " 公尺", D(d + 1) + " 公尺"],
                   "%s比較少，用減法：%s － %s ＝ %s（公尺）。" % (o, D(a), D(b), D(d)))

    def shop():
        a, b = R.randint(105, 499), R.randint(105, 499)
        who = NM.next()
        q = "%s買了 %s 公斤的蘋果和 %s 公斤的香蕉，一共幾公斤？" % (who, D(a), D(b))
        s = a + b
        return mcq(q, D(s) + " 公斤", [D(s + 100) + " 公斤", D(s - 10) + " 公斤", D(s + 10) + " 公斤", D(abs(a - b)) + " 公斤"],
                   "%s ＋ %s ＝ %s（公斤）。" % (D(a), D(b), D(s)))

    def water():
        per = R.randint(15, 95)
        n = R.randint(3, 8)
        if per % 10 == 0:
            return None
        q = "每天喝 %s 公升的牛奶，%d 天一共喝幾公升？" % (D(per), n)
        v = per * n
        return mcq(q, D(v) + " 公升", [D(v * 10) + " 公升", D(v + per) + " 公升", D(per + n) + " 公升", D(v - per) + " 公升"],
                   "%s × %d ＝ %s（公升）。" % (D(per), n, D(v)))
    return pick_unique(R, jump, 7, seen) + pick_unique(R, shop, 7, seen) + pick_unique(R, water, 6, seen)


def main():
    seen = set()
    sets = [("百分位和 0.01", s1(seen)), ("比大小", s2(seen)), ("二位小數的加減", s3(seen)),
            ("整數倍和單位換算", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["把 1 平分成 100 份，1 份是 <b>0.01</b>（%s）。小數點右邊第二位叫<b>百分位</b>。" % fr(1, 100),
         "2.35 是 2 個 1、3 個 0.1、5 個 0.01，也是 235 個 0.01。",
         "比大小：從個位開始一位一位比，<b>不是看小數有幾位</b>：0.8 ＞ 0.65。",
         "直式加減：<b>小數點對齊</b>，從百分位算起。"],
        [example("3.47 ＋ 1.8 ＝", ["小數點對齊：1.8 看成 1.80。", "7 ＋ 0 ＝ 7；4 ＋ 8 ＝ 12，寫 2 進 1；3 ＋ 1 ＋ 1 ＝ 5。"], "5.27"),
         example("0.8 和 0.65 哪一個大？", ["0.8 ＝ 0.80。", "十分位 8 ＞ 6。"], "0.8 比較大")],
        [("0.65 比 0.8 大（因為有兩位）", "0.8 ＝ 0.80，十分位 8 比 6 大"),
         ("3.47 ＋ 1.8 把 8 對齊 7，算成 3.55", "小數點要對齊：1.8 的 8 在十分位"),
         ("0.07 寫成 0.7", "7 個 0.01 是 0.07")])
    faq = [{"q": "四年級的小數要學什麼？",
            "a": "108課綱 N-4-7：認識二位小數和百分位，做位值單位換算，會比較大小，用直式計算二位小數的加減和整數倍。"},
           {"q": "為什麼 0.8 比 0.65 大？",
            "a": "0.8 ＝ 0.80，是 80 個 0.01；0.65 是 65 個 0.01。比小數要從高位比起，不是比位數多少。"},
           {"q": "小數加減要注意什麼？",
            "a": "小數點一定要對齊。位數不一樣時，可以在後面補 0（1.8 → 1.80），再從右邊算起。"}]
    make_unit(R, "grade-4", "decimals", "N-4-7",
              "二位小數：位值單位「百分位」。位值單位換算。比較、計算與解題。用直式計算二位小數的加、減與整數倍。",
              "二位小數：百分位、比大小與加減",
              "四年級數學 二位小數 練習題｜百分位・小數比大小・小數加減直式 學習單（附解答）",
              "二位小數",
              "國小四年級數學「二位小數」免費學習單：百分位和0.01、比大小、二位小數的加減直式、整數倍、公分和公尺的換算與應用題。100題線上練習馬上對答案，附可列印解答。",
              "小數點對齊，從百分位算起",
              "比小數從個位一位一位比，不是看有幾位。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
