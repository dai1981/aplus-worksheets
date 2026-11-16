# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：圓形圖（108課綱 D-6-1）
  python3 tools/gen_tw_math_g6_pie_charts.py
圓形圖の報讀（百分率）、部分の量＝全體×百分率、全體を求める、圓心角＝百分率×360、百分率を求めて製作（百格の圓形圖）、比較・說明。
誤答：百分率をそのまま人數とする、圓心角で ×360 を忘れる、合計が 100% にならない。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, num, dnum, fig, svg_wrap, text

R = random.Random(61018)
NM = Names(R)
COLS = ["#2e7d4f", "#3f7fbf", "#e0a030", "#c0504d", "#8064a2", "#4bacc6"]
THEMES = [("全班最喜歡的運動", ["籃球", "躲避球", "跑步", "游泳", "桌球"], "人"),
          ("一個月的零用錢用途", ["存錢", "買文具", "買零食", "買書", "其他"], "元"),
          ("全校學生上學的方式", ["走路", "家長接送", "騎腳踏車", "搭公車", "其他"], "人"),
          ("一天的時間分配", ["睡覺", "上學", "玩", "寫作業", "其他"], "小時"),
          ("農場的動物", ["雞", "鴨", "牛", "羊", "豬"], "隻")]


def pcts(k):
    while True:
        cut = sorted(R.sample(range(1, 20), k - 1))
        parts = [b - a for a, b in zip([0] + cut, cut + [20])]
        ps = [p * 5 for p in parts]
        if len(set(ps)) == k and min(ps) >= 5 and max(ps) <= 60:
            return ps


def pie(title, cats, ps):
    W, H, cx, cy, r = 300, 210, 105, 110, 85
    s = [text(W / 2, 16, title, 13)]
    a0 = -90.0
    for i, (c, p) in enumerate(zip(cats, ps)):
        a1 = a0 + p * 3.6
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        big = 1 if p > 50 else 0
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='1.5'/>" % (cx, cy, x0, y0, r, r, big, x1, y1, COLS[i]))
        mid = math.radians((a0 + a1) / 2)
        if p >= 10:
            s.append(text(cx + r * .62 * math.cos(mid), cy + r * .62 * math.sin(mid) + 4, "%d%%" % p, 11, col="#fff"))
        a0 = a1
    for i, (c, p) in enumerate(zip(cats, ps)):
        y = 50 + i * 24
        s.append("<rect x='205' y='%d' width='12' height='12' fill='%s'/>" % (y - 10, COLS[i]))
        s.append(text(222, y, "%s %d%%" % (c, p), 12, anchor="start"))
    svg = svg_wrap(W, H, "".join(s), title + "圓形圖")
    return fig(svg.replace("<svg ", "<svg data-pf='lg' ", 1))


def data():
    t, cats, u = R.choice(THEMES)
    k = R.choice([3, 4, 5])
    return t, cats[:k], u, pcts(k)


def s1(seen):
    def mk():
        t, cats, u, ps = data()
        i = R.randrange(len(cats))
        g = pie(t, cats, ps)
        kind = R.choice(["read", "max", "sum"])
        if kind == "read":
            q = "看圓形圖，「%s」占全部的百分之幾？" % cats[i] + g
            return mcq(q, "%d%%" % ps[i], ["%d%%" % x for x in (100 - ps[i], ps[i] + 5, ps[i] * 2 if ps[i] * 2 <= 100 else ps[i] - 5)  if x != ps[i]], "圖上「%s」標示 %d%%。" % (cats[i], ps[i]))
        if kind == "max":
            m = max(ps)
            ans = cats[ps.index(m)]
            return mcq("看圓形圖，哪一項占的比例最大？" + g, ans, [c for c in cats if c != ans][:3] if len(cats) > 3 else [c for c in cats if c != ans] + ["一樣大"], "扇形最大的是「%s」（%d%%）。" % (ans, m))
        j = (i + 1) % len(cats)
        v = ps[i] + ps[j]
        return mcq("看圓形圖，「%s」和「%s」合起來占百分之幾？" % (cats[i], cats[j]) + g, "%d%%" % v, ["%d%%" % x for x in (100 - v, abs(ps[i] - ps[j]) if ps[i] != ps[j] else v + 10, v + 5)  if x != v and x > 0], "%d%% ＋ %d%% ＝ %d%%。" % (ps[i], ps[j], v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        t, cats, u, ps = data()
        tot = R.choice([20, 40, 60, 80, 120, 200, 300, 400, 500, 800, 1000]) if u != "小時" else 24
        if u == "小時":
            ps = R.choice([[50, 25, 15, 10][:len(cats)]]) if False else None
            if len(cats) != 4:
                return None
            ps = R.choice([[40, 25, 15, 20], [35, 30, 10, 25], [45, 25, 20, 10]])
            ps = [p for p in ps]
            if any((tot * p) % 100 for p in ps):
                ps = [50, 25, 0, 25]
                return None
        i = R.randrange(len(cats))
        v = tot * ps[i] / 100
        if v != int(v):
            return None
        v = int(v)
        g = pie(t, cats, ps)
        q = "這是「%s」的圓形圖，全部共 %s %s。「%s」是多少%s？" % (t, num(tot), u, cats[i], u) + g
        return mcq(q, "%s %s" % (num(v), u), ["%s %s" % (num(x), u) for x in (ps[i], tot - v, v * 2)  if x != v and x > 0] + ["%s %s" % (num(v + 5), u)], "%s × %d%% ＝ %s × %s ＝ %s（%s）。" % (num(tot), ps[i], num(tot), dnum(ps[i] / 100, 2), num(v), u))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        p = R.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75])
        part = R.randint(3, 60)
        tot = part * 100 / p
        if tot != int(tot):
            return None
        tot = int(tot)
        who = R.choice(["喜歡游泳的有", "搭公車上學的有", "參加社團的有", "戴眼鏡的有"])
        q = "一張圓形圖中，%s %d 人，占全部的 %d%%。全部有幾人？" % (who, part, p)
        return mcq(q, "%d 人" % tot, ["%s 人" % num(x) for x in (part * p // 100 if part * p % 100 == 0 else part + p, part + p, tot * 2)  if x != tot], "全部 ＝ 部分 ÷ 百分率：%d ÷ %s ＝ %d（人）。" % (part, dnum(p / 100, 2), tot))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def angle():
        p = R.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75, 80])
        v = p * 360 // 100
        if p * 360 % 100:
            return None
        q = "畫圓形圖時，占 %d%% 的部分，扇形的圓心角是幾度？" % p
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (p, p * 3, 360 - v)  if x != v], "整個圓是 360 度：360 × %d%% ＝ %d（度）。" % (p, v))

    def make():
        t, cats, u = R.choice(THEMES)[:3]
        k = 4
        cats = cats[:k]
        ps = pcts(k)
        tot = R.choice([20, 40, 60, 80, 100, 200])
        vals = [tot * p // 100 for p in ps]
        if any(tot * p % 100 for p in ps):
            return None
        i = R.randrange(k)
        tb = table(["項目"] + cats + ["合計"], [["%s（%s）" % ("數量", u)] + [str(v) for v in vals] + [str(tot)]])
        q = "要把下表畫成圓形圖，「%s」要占百分之幾？" % cats[i] + tb
        return mcq(q, "%d%%" % ps[i], ["%d%%" % x for x in (vals[i], ps[i] + 5, 100 - ps[i])  if x != ps[i]] + ["%d%%" % (ps[i] + 10)], "%d ÷ %d ＝ %s ＝ %d%%。" % (vals[i], tot, dnum(ps[i] / 100, 2), ps[i]))
    return pick_unique(R, angle, 8, seen) + pick_unique(R, make, 12, seen)


def s5(seen):
    def which():
        F_ = [("要表示「全班同學最喜歡的水果各占多少比例」，用哪一種圖最合適？", "圓形圖", ["折線圖", "長條圖", "數線"], "看各部分占全體的比例，用圓形圖最清楚。"),
              ("要看「一年中每個月的氣溫變化」，用哪一種圖最合適？", "折線圖", ["圓形圖", "長條圖", "地圖"], "看隨時間的變化用折線圖。"),
              ("圓形圖中所有百分率加起來是多少？", "100%", ["360%", "50%", "不一定"], "全部就是 100%。"),
              ("圓形圖中，扇形越大表示什麼？", "占全體的比例越大", ["數量越少", "時間越長", "和比例無關"], "扇形大小代表占全體的比例。"),
              ("圓形圖中 25% 的扇形是圓的幾分之幾？", "四分之一", ["二分之一", "五分之一", "四分之三"], "25% ＝ 1/4。"),
              ("圓形圖中 50% 的扇形，圓心角是幾度？", "180 度", ["90 度", "50 度", "360 度"], "360 × 50% ＝ 180。")]
        return mcq(*R.choice(F_))

    def other():
        t, cats, u, ps = data()
        g = pie(t, cats[:-1] + ["？"], ps)
        q = "看圓形圖，「？」占百分之幾？" + g
        v = ps[-1]
        return mcq(q, "%d%%" % v, ["%d%%" % x for x in (100 - v, v + 10, 360 - sum(ps[:-1]) if 360 - sum(ps[:-1]) != v else v + 5)  if x != v], "全部是 100%%：100%% －（%s）＝ %d%%。" % (" ＋ ".join("%d%%" % p for p in ps[:-1]), v))

    def compare():
        t, cats, u, ps = data()
        i, j = R.sample(range(len(cats)), 2)
        if ps[i] == ps[j]:
            return None
        tot = R.choice([200, 400, 500, 1000])
        d = tot * abs(ps[i] - ps[j]) // 100
        g = pie(t, cats, ps)
        q = "這是「%s」的圓形圖，全部共 %s %s。「%s」比「%s」多多少%s？" % (t, num(tot), u, cats[i] if ps[i] > ps[j] else cats[j], cats[j] if ps[i] > ps[j] else cats[i], u) + g
        return mcq(q, "%s %s" % (num(d), u), ["%s %s" % (num(x), u) for x in (abs(ps[i] - ps[j]), d * 2, tot * max(ps[i], ps[j]) // 100)  if x != d], "相差 %d%%：%s × %d%% ＝ %s（%s）。" % (abs(ps[i] - ps[j]), num(tot), abs(ps[i] - ps[j]), num(d), u))
    return pick_unique(R, which, 6, seen) + pick_unique(R, other, 7, seen) + pick_unique(R, compare, 7, seen)


def main():
    seen = set()
    sets = [("報讀圓形圖", s1(seen)), ("求部分的數量", s2(seen)), ("求全體的數量", s3(seen)),
            ("製作圓形圖", s4(seen)), ("說明和比較", s5(seen))]
    body = lesson(
        ["<b>圓形圖</b>把全體看成一個圓（100%），每個扇形表示一部分占全體的比例。",
         "部分的數量 ＝ 全體 × 百分率；全體 ＝ 部分 ÷ 百分率。",
         "製作：先算每一項占全體的百分率（部分 ÷ 全體），在百格的圓形圖上畫出；圓心角 ＝ 360 × 百分率。"],
        [example("全班 40 人，喜歡籃球的占 25%，有幾人？", ["40 × 0.25 ＝ 10。"], "10 人"),
         example("某項占 30%，扇形的圓心角是幾度？", ["360 × 0.3 ＝ 108。"], "108 度")],
        [("占 25% 就是 25 人", "要用全體 × 25%"),
         ("各項百分率加起來不是 100%", "全部一定是 100%"),
         ("圓心角 ＝ 百分率的數字", "要 × 360")])
    faq = [{"q": "圓形圖和長條圖有什麼不同？",
            "a": "圓形圖看各部分占全體的比例，長條圖比較各項目的數量多少。"},
           {"q": "怎麼畫圓形圖？",
            "a": "先算出每一項的百分率，再在已分成 100 格的圓上，依百分率塗出扇形，最後寫上項目和百分率。"},
           {"q": "六年級的圓形圖要學什麼？",
            "a": "108課綱 D-6-1：報讀、說明與製作生活中的圓形圖，包含以百分率分配的圓形圖。"}]
    make_unit(R, "grade-6", "pie-charts", "D-6-1",
              "圓形圖：報讀、說明與製作生活中的圓形圖。包含以百分率分配之圓形圖（製作時應提供學生已分成百格的圓形圖）。",
              "圓形圖",
              "六年級數學 圓形圖 練習題｜百分率・圓心角・報讀與製作 學習單（附解答）",
              "圓形圖",
              "國小六年級數學「圓形圖」免費學習單：報讀圓形圖的百分率、求部分和全體的數量、算出百分率和圓心角來製作圓形圖，以及說明和比較。100題線上練習馬上對答案，附可列印解答。",
              "全體是 100%，部分 ＝ 全體 × 百分率",
              "圓心角 ＝ 360 × 百分率。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
