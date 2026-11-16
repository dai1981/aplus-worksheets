# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：長條圖與折線圖（108課綱 D-4-1）
  python3 tools/gen_tw_math_g4_bar_and_line_graphs.py
長條圖の報讀（1格の値を読む）、比較・合計、折線圖の報讀（気温・身長）、増減の大きい区間、長條圖の作り方（1格をいくつにするか）。
誤答：1 格を 1 と読む、目盛りの線ではなくマスを数え間違える、最も増えた区間を最も高い点と取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK, RED, BLUE

R = random.Random(41024)
NM = Names(R)

THEMES = [("三年級各班借書的本數", ["甲班", "乙班", "丙班", "丁班", "戊班"], "本"),
          ("最喜歡的水果", ["蘋果", "香蕉", "芒果", "西瓜", "葡萄"], "人"),
          ("一週賣出的便當", ["星期一", "星期二", "星期三", "星期四", "星期五"], "個"),
          ("各年級的回收瓶數", ["一年級", "二年級", "三年級", "四年級", "五年級"], "個")]


def bar_svg(title, cats, vals, step, u):
    top = (max(vals) // step + 2) * step
    H, W0, BW, G = 200, 50, 44, 22
    n = len(cats)
    W = W0 + n * (BW + G) + 10
    s = [text(W / 2, 16, "%s（單位：%s）" % (title, u), 13)]
    ticks = top // step
    for i in range(ticks + 1):
        y = 30 + H - H * i / ticks
        s.append(line(W0, y, W - 10, y, "#d8d8d8" if i else INK, 1))
        s.append(text(W0 - 6, y + 4, str(i * step), 11, anchor="end"))
    for k, (c, v) in enumerate(zip(cats, vals)):
        x = W0 + 12 + k * (BW + G)
        h = H * v / top
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, 30 + H - h, BW, h, FILL, GREEN))
        s.append(text(x + BW / 2, 30 + H + 16, c, 11))
    s.append(line(W0, 30, W0, 30 + H, INK, 1.5))
    return fig(svg_wrap(int(W), H + 56, "".join(s), title + "長條圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def line_svg(title, labels, vals, lo, step, u):
    top = lo + (max(vals) - lo) // step * step + 2 * step
    H, W0, GX = 180, 50, 62
    n = len(labels)
    W = W0 + (n - 1) * GX + 40
    s = [text(W / 2, 16, "%s（單位：%s）" % (title, u), 13)]
    ticks = (top - lo) // step
    for i in range(ticks + 1):
        y = 30 + H - H * i / ticks
        s.append(line(W0, y, W - 16, y, "#d8d8d8" if i else INK, 1))
        s.append(text(W0 - 6, y + 4, str(lo + i * step), 11, anchor="end"))
    pts = []
    for k, (c, v) in enumerate(zip(labels, vals)):
        x = W0 + 20 + k * GX
        y = 30 + H - H * (v - lo) / (top - lo)
        pts.append((x, y))
        s.append(text(x, 30 + H + 16, c, 11))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), BLUE))
    s += ["<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (x, y, BLUE) for x, y in pts]
    s.append(line(W0, 30, W0, 30 + H, INK, 1.5))
    if lo:
        s.append(text(W0 - 6, 30 + H + 16, "≈", 12, anchor="end"))
    return fig(svg_wrap(int(W), H + 56, "".join(s), title + "折線圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def bar_data():
    title, cats, u = R.choice(THEMES)
    step = R.choice([2, 5, 10])
    k = R.randint(4, 5)
    vals = [step * R.randint(1, 9) + (step // 2 if step >= 10 and R.random() < .3 else 0) for _ in range(k)]
    if len(set(vals)) < k:
        return None
    return title, cats[:k], vals, step, u


def s1(seen):
    def mk():
        d = bar_data()
        if not d:
            return None
        title, cats, vals, step, u = d
        i = R.randrange(len(cats))
        v = vals[i]
        q = "看長條圖，%s是多少%s？" % (cats[i], u) + bar_svg(title, cats, vals, step, u)
        return mcq(q, "%d %s" % (v, u), ["%d %s" % (x, u) for x in (v // step, v + step, v - step if v > step else v + 2 * step, v + step // 2 if step > 2 else v + 1) if x != v],
                   "先看 1 格代表 %d %s，%s的長條到 %d。" % (step, u, cats[i], v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        d = bar_data()
        if not d:
            return None
        title, cats, vals, step, u = d
        g = bar_svg(title, cats, vals, step, u)
        kind = R.choice(["max", "diff", "sum", "times"])
        if kind == "max":
            ans = cats[vals.index(max(vals))]
            return mcq("看長條圖，哪一項最多？" + g, ans, [c for c in cats if c != ans], "長條最高的是%s（%d %s）。" % (ans, max(vals), u))
        i, j = R.sample(range(len(cats)), 2)
        if kind == "diff":
            if vals[i] < vals[j]:
                i, j = j, i
            dv = vals[i] - vals[j]
            return mcq("看長條圖，%s比%s多多少%s？" % (cats[i], cats[j], u) + g, "%d %s" % (dv, u), ["%d %s" % (x, u) for x in (vals[i] + vals[j], dv // step if dv // step != dv else dv + step, dv + step) if x != dv],
                       "%d － %d ＝ %d（%s）。" % (vals[i], vals[j], dv, u))
        if kind == "sum":
            t = sum(vals)
            return mcq("看長條圖，全部一共多少%s？" % u + g, "%d %s" % (t, u), ["%d %s" % (x, u) for x in (t - vals[-1], t + step, sum(v // step for v in vals))],
                       "全部加起來：%s ＝ %d（%s）。" % (" ＋ ".join(map(str, vals)), t, u))
        if vals[j] == 0 or vals[i] % vals[j] or vals[i] == vals[j]:
            return None
        k = vals[i] // vals[j]
        return mcq("看長條圖，%s是%s的幾倍？" % (cats[i], cats[j]) + g, "%d 倍" % k, ["%d 倍" % x for x in (k + 1, vals[i] - vals[j], k * 2) if x != k], "%d ÷ %d ＝ %d（倍）。" % (vals[i], vals[j], k))
    return pick_unique(R, mk, 20, seen)


def line_data():
    kind = R.choice(["temp", "height", "rain"])
    if kind == "temp":
        labels = ["6 時", "9 時", "12 時", "15 時", "18 時"]
        base = R.randint(14, 20)
        vals = [base + x for x in (0, R.randint(2, 5), R.randint(6, 10), R.randint(5, 9), R.randint(1, 4))]
        return "一天的氣溫", labels, vals, base - 2, 1, "度"
    if kind == "height":
        labels = ["第 1 週", "第 2 週", "第 3 週", "第 4 週", "第 5 週"]
        h = R.randint(1, 3) * 2
        vals = [h]
        for _ in range(4):
            vals.append(vals[-1] + R.choice([2, 4, 6]))
        return "豆苗的高度", labels, vals, 0, 2, "公分"
    labels = ["1 月", "2 月", "3 月", "4 月", "5 月", "6 月"]
    vals = [R.randint(2, 30) * 10 for _ in labels]
    return "每月的雨量", labels, vals, 0, 50, "毫米"


def s3(seen):
    def mk():
        title, labels, vals, lo, step, u = line_data()
        i = R.randrange(len(labels))
        v = vals[i]
        if v % step and step > 2:
            return None
        q = "看折線圖，%s的%s是多少？" % (labels[i], title.replace("一天的", "").replace("每月的", "").replace("豆苗的", "豆苗")) + line_svg(title, labels, vals, lo, step, u)
        return mcq(q, "%d %s" % (v, u), ["%d %s" % (x, u) for x in (v + step, v - step, v + step // 2 if step > 2 else v + 1, (v - lo) // step) if x != v and x >= 0],
                   "找到%s，點對到左邊的刻度：%d %s。（1 格是 %d）" % (labels[i], v, u, step))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        title, labels, vals, lo, step, u = line_data()
        if any(v % step for v in vals) and step > 2:
            return None
        g = line_svg(title, labels, vals, lo, step, u)
        diffs = [vals[k + 1] - vals[k] for k in range(len(vals) - 1)]
        kind = R.choice(["up", "max", "range"])
        if kind == "up":
            m = max(diffs)
            if diffs.count(m) > 1 or m <= 0:
                return None
            k = diffs.index(m)
            ans = "%s到%s" % (labels[k], labels[k + 1])
            w = ["%s到%s" % (labels[j], labels[j + 1]) for j in range(len(diffs)) if j != k]
            return mcq("看折線圖，哪兩個時間之間增加得最多？" + g, ans, w, "線最陡（往上最多）的一段：%s，增加 %d %s。" % (ans, m, u))
        if kind == "max":
            mx = max(vals)
            if vals.count(mx) > 1:
                return None
            ans = labels[vals.index(mx)]
            return mcq("看折線圖，什麼時候最高？" + g, ans, [l for l in labels if l != ans][:3], "折線最高的點是%s（%d %s）。" % (ans, mx, u))
        d = max(vals) - min(vals)
        return mcq("看折線圖，最高和最低相差多少%s？" % u + g, "%d %s" % (d, u), ["%d %s" % (x, u) for x in (max(vals), d + step, d - step if d > step else d + 2 * step, d // step if d // step != d else d + 1) if x != d],
                   "%d － %d ＝ %d（%s）。" % (max(vals), min(vals), d, u))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def scale():
        mx = R.choice([18, 24, 35, 48, 60, 85, 120, 180, 240, 300])
        q = "要畫長條圖，資料最大是 %d，圖上最多只能畫 15 格。1 格代表多少最合適？" % mx
        opts = [1, 2, 5, 10, 20, 50]
        good = min(o for o in opts if mx / o <= 15)
        w = [o for o in opts if o != good]
        w = sorted(w, key=lambda o: abs(o - good))[:3]
        return mcq(q, "1 格代表 %d" % good, ["1 格代表 %d" % o for o in w], "%d ÷ %d %s %d 格，不超過 15 格，又不會太少，最合適。" % (mx, good, "＝" if mx % good == 0 else "≈", -(-mx // good)))

    def cells():
        step = R.choice([2, 5, 10, 20])
        v = step * R.randint(2, 12)
        q = "長條圖 1 格代表 %d，%d 要畫幾格？" % (step, v)
        return mcq(q, "%d 格" % (v // step), ["%d 格" % x for x in (v, v // step + 1, v * step if v * step < 500 else v // step * 2)], "%d ÷ %d ＝ %d（格）。" % (v, step, v // step))

    def which():
        F = [("要看一天中氣溫怎麼變化，用哪一種圖最合適？", "折線圖", ["長條圖", "圓形圖", "表格就好，不用畫圖"], "要看變化（上升、下降）用折線圖。"),
             ("要比較各班借書的本數誰多誰少，用哪一種圖最合適？", "長條圖", ["折線圖", "數線", "地圖"], "要比較各項目的多少用長條圖。"),
             ("要看豆苗每週長高的情形，用哪一種圖最合適？", "折線圖", ["長條圖", "地圖", "數線"], "隨時間變化的資料用折線圖。"),
             ("要比較最喜歡的水果哪一種人數最多，用哪一種圖最合適？", "長條圖", ["折線圖", "數線", "地圖"], "比較各項目的多少用長條圖。"),
             ("折線圖中，線往右上方走代表什麼？", "數量增加", ["數量減少", "數量不變", "資料錯了"], "往右上方是增加，往右下方是減少，平的是不變。"),
             ("折線圖中，線往右下方走代表什麼？", "數量減少", ["數量增加", "數量不變", "資料錯了"], "往右下方是減少。")]
        return mcq(*R.choice(F))
    return pick_unique(R, scale, 7, seen) + pick_unique(R, cells, 7, seen) + pick_unique(R, which, 6, seen)


def main():
    seen = set()
    sets = [("讀長條圖", s1(seen)), ("用長條圖比較", s2(seen)), ("讀折線圖", s3(seen)),
            ("折線圖的變化", s4(seen)), ("畫圖和選圖", s5(seen))]
    body = lesson(
        ["讀圖前先看<b>標題、單位</b>和<b>1 格代表多少</b>。",
         "<b>長條圖</b>適合比較各項目的多少；<b>折線圖</b>適合看數量隨時間的變化。",
         "折線往右上是增加，往右下是減少，<b>線越陡變化越大</b>。",
         "畫長條圖時，先看最大的資料，決定 1 格代表多少，格子不要太多也不要太少。"],
        [example("長條圖 1 格代表 5 本，甲班的長條有 7 格，借了幾本？", ["5 × 7 ＝ 35。"], "35 本"),
         example("氣溫 9 時 18 度、12 時 25 度，增加多少？", ["25 － 18 ＝ 7。"], "7 度")],
        [("1 格當成 1", "先看左邊的刻度：1 格可能是 2、5、10"),
         ("最高的點就是增加最多的地方", "增加最多要看哪一段線最陡"),
         ("沒看單位就回答", "先看標題旁的單位：本、人、度、公分")])
    faq = [{"q": "長條圖和折線圖有什麼不同？",
            "a": "長條圖用長條的長短比較各項目的多少；折線圖用線的上下表示數量隨時間的變化，適合看增加或減少。"},
           {"q": "四年級的統計圖要學什麼？",
            "a": "108課綱 D-4-1：報讀和說明生活中的長條圖與折線圖，並學習製作長條圖。"},
           {"q": "畫長條圖時 1 格要代表多少？",
            "a": "看最大的數和紙上可以畫幾格：最大的數 ÷ 1 格代表的數，不要超過可以畫的格數，又不要太少，常用 1、2、5、10。"}]
    make_unit(R, "grade-4", "bar-and-line-graphs", "D-4-1",
              "報讀長條圖與折線圖以及製作長條圖：報讀與說明生活中的長條圖與折線圖。配合其他領域課程，學習製作長條圖。",
              "長條圖與折線圖：報讀與製作",
              "四年級數學 長條圖 折線圖 練習題｜報讀統計圖・畫長條圖 學習單（附解答）",
              "長條圖與折線圖",
              "國小四年級數學「長條圖與折線圖」免費學習單：讀長條圖、用長條圖比較、讀折線圖和變化、決定1格代表多少和選擇合適的圖。100題線上練習馬上對答案，附可列印解答。",
              "先看 1 格代表多少",
              "長條圖比多少，折線圖看變化。",
              body, faq, sets, 24)


if __name__ == "__main__":
    main()
