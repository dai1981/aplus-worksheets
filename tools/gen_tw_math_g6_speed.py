# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：速度（108課綱 N-6-7）
  python3 tools/gen_tw_math_g6_speed.py
速度＝距離÷時間（秒速・分速・時速）、距離＝速度×時間、時間＝距離÷速度、單位換算（時速→分速→秒速）、不同時間區段的平均速度。
誤答：時間÷距離にする、平均速度を速度の平均で出す、時速→分速で ×60 にする、公里と公尺をそろえない。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num, ff, dnum

R = random.Random(61007)
NM = Names(R)

MOVERS = [("走路", 50, 90, "分速", "公尺"), ("騎腳踏車", 180, 300, "分速", "公尺"), ("跑步", 3, 7, "秒速", "公尺"),
          ("汽車", 40, 90, "時速", "公里"), ("火車", 60, 130, "時速", "公里"), ("高鐵", 200, 300, "時速", "公里")]
TU = {"分速": "分鐘", "秒速": "秒", "時速": "小時"}


def s1(seen):
    def mk():
        what, lo, hi, kind, u = R.choice(MOVERS)
        v = R.randint(lo, hi)
        if kind == "時速":
            v = v // 5 * 5
        t = R.randint(2, 15) if kind != "時速" else R.randint(2, 5)
        if kind == "秒速":
            t = R.randint(10, 60)
        d = v * t
        if what == "高鐵" and d > 350:
            return None
        who = NM.next()
        verb = {"走路": "走了", "騎腳踏車": "騎了", "跑步": "跑了"}.get(what)
        if verb:
            q = "%s%s，%d %s%s %s %s。%s是多少？" % (who, what, t, TU[kind], verb, num(d), u, kind)
        else:
            q = "一列%s %d %s開了 %s %s。%s是多少？" % (what, t, TU[kind], num(d), u, kind) if what != "汽車" else "一輛汽車 %d %s開了 %s %s。時速是多少？" % (t, TU[kind], num(d), u)
        return mcq(q, "%s %d %s" % (kind, v, u), ["%s %s %s" % (kind, ff(F(t, d)) if False else num(d * t), u), "%s %d %s" % (kind, v + t, u), "%s %d %s" % (kind, d - t, u)],
                   "速度 ＝ 距離 ÷ 時間：%s ÷ %d ＝ %d，%s %d %s。" % (num(d), t, v, kind, v, u))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def dist():
        what, lo, hi, kind, u = R.choice(MOVERS)
        v = R.randint(lo, hi)
        if kind == "時速":
            v = v // 5 * 5
        t = R.randint(3, 25) if kind != "時速" else R.choice([F(3, 2), F(5, 2), 2, 3, 4, F(1, 2)])
        d = v * F(t)
        if what == "高鐵" and d > 350:
            return None
        ts = "%s 小時" % ff(F(t), mixed=False) if kind == "時速" and F(t).denominator != 1 else "%s %s" % (ff(F(t)), TU[kind])
        if kind == "時速" and F(t).denominator != 1:
            ts = "%s 小時" % dnum(float(t))
        q = "%s的%s是 %d %s，%s可以前進多少%s？" % (what, kind, v, u, ts, u)
        g = lambda x: dnum(float(x))
        return mcq(q, "%s %s" % (g(d), u), ["%s %s" % (g(x), u) for x in (d - v if d > v else d + 2 * v, v + F(t), d + v)], "距離 ＝ 速度 × 時間：%d × %s ＝ %s（%s）。" % (v, g(t), g(d), u))

    def time():
        what, lo, hi, kind, u = R.choice(MOVERS)
        v = R.randint(lo, hi)
        if kind == "時速":
            v = v // 10 * 10
        t = R.randint(2, 12)
        d = v * t
        if (what == "高鐵" and d > 350) or (kind == "時速" and t > 6):
            return None
        q = "%s的%s是 %d %s，要走 %s %s，需要多少%s？" % (what, kind, v, u, num(d), u, TU[kind])
        return mcq(q, "%d %s" % (t, TU[kind]), ["%s %s" % (num(x), TU[kind]) for x in (d * v if d * v < 10 ** 6 else d + v, d - v, t + 1)], "時間 ＝ 距離 ÷ 速度：%s ÷ %d ＝ %d（%s）。" % (num(d), v, t, TU[kind]))
    return pick_unique(R, dist, 10, seen) + pick_unique(R, time, 10, seen)


def s3(seen):
    def h2m():
        v = R.choice([36, 48, 54, 60, 72, 90, 108, 120, 144, 180])
        m = v * 1000 // 60
        if v * 1000 % 60:
            return None
        q = "時速 %d 公里，等於分速多少公尺？" % v
        return mcq(q, "分速 %s 公尺" % num(m), ["分速 %s 公尺" % num(x) for x in (v * 60, v * 1000 * 60 if False else v * 60 * 1000 // 1000 * 10, v * 1000)] if True else [],
                   "1 公里 ＝ 1000 公尺，1 小時 ＝ 60 分鐘：%d × 1000 ÷ 60 ＝ %s（公尺）。" % (v, num(m)))

    def m2s():
        v = R.choice([60, 120, 180, 240, 300, 360, 420, 480, 540, 600])
        s = v // 60
        q = "分速 %d 公尺，等於秒速多少公尺？" % v
        return mcq(q, "秒速 %d 公尺" % s, ["秒速 %s 公尺" % num(x) for x in (v * 60, v // 10, s + 60)], "1 分鐘 ＝ 60 秒：%d ÷ 60 ＝ %d（公尺）。" % (v, s))

    def m2h():
        v = R.choice([50, 60, 75, 80, 100, 150, 200, 250, 300, 500])
        h = F(v * 60, 1000)
        q = "分速 %d 公尺，等於時速多少公里？" % v
        return mcq(q, "時速 %s 公里" % dnum(float(h)), ["時速 %s 公里" % x for x in (num(v * 60), dnum(v / 60, 2), dnum(float(h) * 10))], "%d × 60 ＝ %s（公尺）＝ %s 公里，時速 %s 公里。" % (v, num(v * 60), dnum(float(h)), dnum(float(h))))
    return pick_unique(R, h2m, 7, seen) + pick_unique(R, m2s, 7, seen) + pick_unique(R, m2h, 6, seen)


def s4(seen):
    def compare():
        a_d, a_t = R.choice([(400, 5), (600, 8), (900, 12), (750, 10), (360, 4)])
        b_d, b_t = R.choice([(500, 6), (480, 5), (700, 10), (840, 12), (300, 3)])
        va, vb = F(a_d, a_t), F(b_d, b_t)
        if va == vb:
            return None
        n1, n2 = NM.next(), NM.next()
        if n1 == n2:
            return None
        q = "%s %d 分鐘走 %d 公尺，%s %d 分鐘走 %d 公尺。誰走得比較快？" % (n1, a_t, a_d, n2, b_t, b_d)
        ans = n1 if va > vb else n2
        oth = n2 if ans == n1 else n1
        return mcq(q, ans, [oth, "一樣快", "走得遠的人比較快"], "比分速：%s %s 公尺，%s %s 公尺，%s比較快。" % (n1, dnum(float(va), 1), n2, dnum(float(vb), 1), ans))

    def avg():
        d1, v1 = R.choice([(120, 60), (90, 45), (150, 50), (100, 50), (80, 40)])
        d2, v2 = R.choice([(60, 30), (120, 40), (100, 25), (90, 30), (60, 20)])
        t = F(d1, v1) + F(d2, v2)
        V = F(d1 + d2) / t
        if V.denominator != 1:
            return None
        q = "汽車先以時速 %d 公里開了 %d 公里，再以時速 %d 公里開了 %d 公里。全程的平均時速是多少公里？" % (v1, d1, v2, d2)
        return mcq(q, "時速 %d 公里" % V, ["時速 %s 公里" % ff(x) for x in ((v1 + v2) / F(2), V + 5, F(d1 + d2, 2))  if x != V],
                   "平均速度 ＝ 總距離 ÷ 總時間：%d ＋ %d ＝ %d（公里），%s ＋ %s ＝ %s（小時），%d ÷ %s ＝ %d。不是把兩個速度平均。" % (d1, d2, d1 + d2, ff(F(d1, v1)), ff(F(d2, v2)), ff(t), d1 + d2, ff(t), V))
    return pick_unique(R, compare, 10, seen) + pick_unique(R, avg, 10, seen)


def s5(seen):
    def train():
        v = R.choice([60, 72, 90, 120, 150, 180])
        start = R.randint(7, 15)
        mins = R.choice([20, 30, 40, 45, 50, 80, 90, 100])
        d = F(v * mins, 60)
        if d.denominator != 1:
            return None
        eh, em = divmod(start * 60 + mins, 60)
        q = "火車以時速 %d 公里行駛，%d 時出發，%d 時 %02d 分到達。兩站相距幾公里？" % (v, start, eh, em) if em else "火車以時速 %d 公里行駛，%d 時出發，%d 時到達。兩站相距幾公里？" % (v, start, eh)
        return mcq(q, "%d 公里" % d, ["%d 公里" % x for x in (v * mins, v * mins // 100 if v * mins // 100 != d else d + v, d + v // 2)], "行駛 %d 分鐘 ＝ %s 小時，%d × %s ＝ %d（公里）。" % (mins, ff(F(mins, 60)), v, ff(F(mins, 60)), d))

    def meet():
        va, vb = R.randint(50, 90), R.randint(50, 90)
        t = R.randint(5, 15)
        d = (va + vb) * t
        n1, n2 = NM.next(), NM.next()
        q = "%s和%s從相距 %s 公尺的兩地同時出發，面對面走。%s分速 %d 公尺，%s分速 %d 公尺。幾分鐘後相遇？" % (n1, n2, num(d), n1, va, n2, vb)
        return mcq(q, "%d 分鐘" % t, ["%s 分鐘" % ff(x) for x in (F(d, abs(va - vb)) if va != vb else F(t * 2), F(d, va), F(t, 2) if t % 2 == 0 else F(t + 2))  if x != t],
                   "兩人每分鐘一共靠近 %d ＋ %d ＝ %d 公尺，%s ÷ %d ＝ %d（分鐘）。" % (va, vb, va + vb, num(d), va + vb, t))

    def ratio():
        v = R.choice([4, 5, 6, 8])
        t1, k = R.randint(10, 30), R.choice([2, 3, 4])
        q = "小狗秒速 %d 公尺，%d 秒跑了 %d 公尺。照同樣的速度，跑 %d 公尺要幾秒？" % (v, t1, v * t1, v * t1 * k)
        return mcq(q, "%d 秒" % (t1 * k), ["%d 秒" % x for x in (t1 + k, v * t1 * k * v // 10 if False else t1 * k * v, t1 * (k + 1))], "距離變成 %d 倍，時間也變成 %d 倍：%d × %d ＝ %d（秒）。" % (k, k, t1, k, t1 * k))
    return pick_unique(R, train, 7, seen) + pick_unique(R, meet, 7, seen) + pick_unique(R, ratio, 6, seen)


def main():
    seen = set()
    sets = [("求速度", s1(seen)), ("求距離和時間", s2(seen)), ("速度的單位換算", s3(seen)),
            ("比快慢和平均速度", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>速度 ＝ 距離 ÷ 時間</b>：每單位時間走的距離。1 小時走的叫時速，1 分鐘的叫分速，1 秒的叫秒速。",
         "<b>距離 ＝ 速度 × 時間</b>；<b>時間 ＝ 距離 ÷ 速度</b>。單位要先對好（公里和公尺、小時和分鐘）。",
         "<b>平均速度 ＝ 總距離 ÷ 總時間</b>，不是把兩個速度加起來除以 2。"],
        [example("時速 72 公里是分速多少公尺？", ["72 公里 ＝ 72000 公尺。", "72000 ÷ 60 ＝ 1200。"], "分速 1200 公尺"),
         example("3 小時走了 210 公里，時速多少？", ["210 ÷ 3 ＝ 70。"], "時速 70 公里")],
        [("速度 ＝ 時間 ÷ 距離", "距離 ÷ 時間"),
         ("時速換分速用 × 60", "1 小時走的距離分成 60 份：÷ 60"),
         ("平均速度 ＝（60 ＋ 30）÷ 2", "總距離 ÷ 總時間")])
    faq = [{"q": "速度的公式怎麼記？",
            "a": "距離 ＝ 速度 × 時間。要求速度就用距離 ÷ 時間，要求時間就用距離 ÷ 速度。"},
           {"q": "時速、分速、秒速怎麼換？",
            "a": "時速 ÷ 60 ＝ 分速，分速 ÷ 60 ＝ 秒速；公里換公尺要 × 1000。例如時速 36 公里 ＝ 分速 600 公尺 ＝ 秒速 10 公尺。"},
           {"q": "六年級的速度要學什麼？",
            "a": "108課綱 N-6-7：速度的意義、單位換算、不同時間區段的平均速度和「距離 ＝ 速度 × 時間」，並用比例思考協助解題。"}]
    make_unit(R, "grade-6", "speed", "N-6-7",
              "解題：速度。比和比值的應用。速度的意義。能做單位換算（大單位到小單位）。含不同時間區段的平均速度。含「距離＝速度×時間」公式。用比例思考協助解題。",
              "速度：時速、分速、秒速",
              "六年級數學 速度 練習題｜時速・分速・秒速・平均速度 學習單（附解答）",
              "速度",
              "國小六年級數學「速度」免費學習單：求速度、距離和時間，時速、分速、秒速的換算，比快慢、平均速度與火車、相遇等應用題。100題線上練習馬上對答案，附可列印解答。",
              "距離 ＝ 速度 × 時間",
              "速度 ＝ 距離 ÷ 時間；平均速度 ＝ 總距離 ÷ 總時間。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
