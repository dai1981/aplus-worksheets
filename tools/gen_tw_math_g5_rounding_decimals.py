# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：對小數取概數（108課綱 N-5-11）
  python3 tools/gen_tw_math_g5_rounding_decimals.py
四捨五入で整數・十分位・百分位に取る、商除不盡の処理、近似の意味（範囲）、生活の應用（身長・價錢・成績）。
誤答：取る位を 1 つずらす、9 の繰り上がりで隣の位を変え忘れる（2.96→2.10）、末尾の 0 を消す（3.0→3）。
"""
import random
from decimal import Decimal as Dm, ROUND_HALF_UP, ROUND_DOWN
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num

R = random.Random(51012)
NM = Names(R)
PL = {"1": "整數（個位）", "0.1": "十分位", "0.01": "百分位"}


def rd(x, q):
    return Dm(x).quantize(Dm(q), rounding=ROUND_HALF_UP)


def S(x):
    """取概數の結果は末尾の 0 を残す"""
    return format(x, "f")


def s_round(seen, q, n):
    def mk():
        places = {"1": 2, "0.1": 2, "0.01": 3}[q]
        x = Dm(R.randint(10 ** places + 1, 99 * 10 ** places)) / Dm(10 ** places)
        if R.random() < .3:
            # 9 の繰り上がりを含む数
            base = rd(x, q)
            x = base + Dm(q) - Dm(1).scaleb(-places) * R.randint(1, 4)
        v = rd(x, q)
        dn = x.quantize(Dm(q), rounding=ROUND_DOWN)
        up = dn + Dm(q)
        other = up if v == dn else dn
        finer = {"1": "0.1", "0.1": "0.01", "0.01": "0.001"}[q]
        w = [S(other), S(rd(x, finer)) if rd(x, finer) != v else S(v + Dm(q)), S(v + Dm(q)) if v + Dm(q) != other else S(v - Dm(q))]
        if q != "1" and S(v).endswith("0"):
            w.append(S(v.normalize()) if "." in S(v.normalize()) else S(v.normalize()))
        return mcq("用四捨五入法，把 %s 取到<b>%s</b>。" % (format(x.normalize(), "f"), PL[q]), S(v), [y for y in w if y != S(v)],
                   "看%s的下一位，%s：%s。%s" % (PL[q].replace("整數（個位）", "個位"), "5 以上進 1" if v == up else "4 以下捨去", S(v),
                                          "（取到%s，最後的 0 要寫）" % PL[q] if q != "1" and S(v).endswith("0") else ""))
    return pick_unique(R, mk, n, seen)


def s4(seen):
    def quot():
        a, b = R.randint(1, 60), R.choice([3, 6, 7, 9, 11, 12, 13])
        if a % b == 0:
            return None
        q = R.choice(["0.1", "0.01"])
        v = rd(Dm(a) / Dm(b), q)
        dn = (Dm(a) / Dm(b)).quantize(Dm(q), rounding=ROUND_DOWN)
        return mcq("%d ÷ %d 的商用四捨五入法取到%s是多少？" % (a, b, PL[q]), S(v), [S(dn) if dn != v else S(v + Dm(q)), S(rd(Dm(a) / Dm(b), "0.001")), S(v * 10)],
                   "多除一位：%d ÷ %d ＝ %s…，再四捨五入：%s。" % (a, b, format((Dm(a) / Dm(b)).quantize(Dm("0.0001"), rounding=ROUND_DOWN), "f"), S(v)))

    def rng():
        v = Dm(R.randint(11, 99)) / 10
        ask = R.choice(["最小", "最大"])
        lo, hi = v - Dm("0.05"), v + Dm("0.04")
        t = lo if ask == "最小" else hi
        q = "一個二位小數用四捨五入法取到十分位是 %s，這個數%s是多少？" % (S(v), ask)
        w = [S(v - Dm("0.04")) if ask == "最小" else S(v + Dm("0.05")), S(v - Dm("0.1")) if ask == "最小" else S(v + Dm("0.09")), S(v)]
        return mcq(q, S(t), w, "%s 到 %s 取到十分位都是 %s，%s是 %s。" % (S(lo), S(hi), S(v), ask, S(t)))
    return pick_unique(R, quot, 12, seen) + pick_unique(R, rng, 8, seen)


def s5(seen):
    def mk():
        kind = R.choice(["height", "price", "avg", "kg"])
        if kind == "height":
            x = Dm(R.randint(1300, 1600)) / 1000
            q = "%s的身高是 %s 公尺，用四捨五入法取到百分位是幾公尺？" % (NM.next(), format(x.normalize(), "f"))
            v = rd(x, "0.01")
            u = "公尺"
        elif kind == "price":
            tot, n = R.randint(100, 999), R.choice([3, 6, 7, 9])
            if tot % n == 0:
                return None
            q = "%d 個杯子蛋糕共 %d 元，一個大約多少元？（四捨五入取到整數）" % (n, tot)
            v = rd(Dm(tot) / n, "1")
            u = "元"
        elif kind == "avg":
            scores = [R.randint(60, 100) for _ in range(3)]
            q = "%s三次考試是 %s 分，平均幾分？（四捨五入取到十分位）" % (NM.next(), "、".join(map(str, scores)))
            v = rd(Dm(sum(scores)) / 3, "0.1")
            if sum(scores) % 3 == 0:
                return None
            u = "分"
        else:
            g = R.randint(1001, 9999)
            q = "%d 公克是幾公斤？（四捨五入取到十分位）" % g
            v = rd(Dm(g) / 1000, "0.1")
            u = "公斤"
        q_ = "1" if kind == "price" else ("0.01" if kind == "height" else "0.1")
        return mcq(q, S(v) + " " + u, [S(v + Dm(q_)) + " " + u, S(v - Dm(q_)) + " " + u, S(v * 10) + " " + u], "四捨五入取概數：%s %s。" % (S(v), u))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("取到整數", s_round(seen, "1", 20)), ("取到十分位", s_round(seen, "0.1", 20)), ("取到百分位", s_round(seen, "0.01", 20)),
            ("除不盡和原來的數", s4(seen)), ("生活中的概數", s5(seen))]
    body = lesson(
        ["取到哪一位，就看它的<b>下一位</b>：0〜4 捨去，5〜9 進 1。",
         "進 1 時如果是 9，要再往前進：2.96 取到十分位是 <b>3.0</b>。",
         "取到十分位的答案要留一位小數，<b>最後的 0 不能省</b>（3.0 表示準確到十分位）。",
         "除不盡時，多除一位再四捨五入。"],
        [example("把 4.267 取到百分位", ["百分位是 6，看下一位千分位 7。", "7 ≥ 5，進 1。"], "4.27"),
         example("把 2.96 取到十分位", ["看百分位 6，進 1。", "十分位 9 ＋ 1 ＝ 10，再進到個位。"], "3.0")],
        [("4.267 取到百分位，看十分位", "看要取的位的下一位：千分位"),
         ("2.96 取到十分位寫成 2.10", "9 進 1 變 10，要再往前進：3.0"),
         ("取到十分位寫成 3", "要留到十分位：3.0")])
    faq = [{"q": "小數怎麼用四捨五入取概數？",
            "a": "取到哪一位就看下一位：小於 5 捨去，5 以上進 1。例如 4.267 取到百分位，看千分位 7，進 1 得 4.27。"},
           {"q": "為什麼 3.0 的 0 不能省略？",
            "a": "3.0 表示取到十分位，準確到 0.1；寫成 3 就變成只取到個位，意思不一樣。"},
           {"q": "五年級的小數概數要學什麼？",
            "a": "108課綱 N-5-11：在生活情境中對小數用四捨五入取概數，知道商除不盡時的處理，並理解近似的意義。"}]
    make_unit(R, "grade-5", "rounding-decimals", "N-5-11",
              "解題：對小數取概數。具體生活情境。四捨五入法。知道商除不盡的處理。理解近似的意義。",
              "小數的概數：四捨五入",
              "五年級數學 小數概數 練習題｜四捨五入到十分位・百分位・除不盡 學習單（附解答）",
              "小數的概數",
              "國小五年級數學「小數的概數」免費學習單：用四捨五入法把小數取到整數、十分位、百分位，處理除不盡和原來的數的範圍與生活應用。100題線上練習馬上對答案，附可列印解答。",
              "看下一位：0〜4 捨，5〜9 進",
              "取到十分位，最後的 0 也要寫。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
