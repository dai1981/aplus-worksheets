# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：製作折線圖（108課綱 D-5-1）
  python3 tools/gen_tw_math_g5_making_line_graphs.py
表から折線圖を作る（點が何格目か・1 格の大きさ・省略符號）、畫錯的點を見つける、報讀と解釋、生活の資料。
誤答：1 格を 1 と数える、省略した下の部分を 0 から数える、增加量と最大値を取り違える。
"""
import random
import re
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, fig, svg_wrap, text, line, INK, BLUE, RED

R = random.Random(51027)
NM = Names(R)


def line_svg(title, labels, vals, lo, step, u, bad=None):
    top = lo + ((max(vals) - lo) // step + 2) * step
    H, W0, GX = 180, 52, 58
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
        y0 = 30 + H + 2
        s.append("<path d='M%d %d l5 -5 l5 10 l5 -5' fill='none' stroke='%s' stroke-width='1.5'/>" % (W0 - 8, y0 - 14, INK))
    return fig(svg_wrap(int(W), H + 56, "".join(s), title + "折線圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def data():
    k = R.choice(["temp", "height", "rain", "weight", "visit"])
    if k == "temp":
        labels = ["8 時", "10 時", "12 時", "14 時", "16 時", "18 時"]
        b = R.randint(18, 24)
        vals = [b + x for x in (0, R.randint(2, 4), R.randint(5, 8), R.randint(7, 10), R.randint(4, 6), R.randint(1, 3))]
        return "一天的氣溫", "氣溫", labels, vals, b - 2, 1, "度"
    if k == "height":
        labels = ["1 歲", "3 歲", "5 歲", "7 歲", "9 歲", "11 歲"]
        v = R.randint(74, 80)
        vals = [v]
        for g in (16, 13, 12, 11, 10):
            vals.append(vals[-1] + g + R.randint(-2, 2))
        vals = [x // 5 * 5 for x in vals]
        if len(set(vals)) < 6:
            return None
        return "小明的身高", "身高", labels, vals, 70, 10, "公分"
    if k == "rain":
        labels = ["3 月", "4 月", "5 月", "6 月", "7 月", "8 月"]
        vals = [R.randint(2, 18) * 20 for _ in labels]
        return "每月的雨量", "雨量", labels, vals, 0, 40, "毫米"
    if k == "weight":
        labels = ["第 1 週", "第 2 週", "第 3 週", "第 4 週", "第 5 週"]
        v = R.randint(6, 9) * 50
        vals = [v]
        for _ in range(4):
            vals.append(vals[-1] + R.choice([25, 50, 75, 100]))
        return "小狗的體重", "體重", labels, vals, (v // 100) * 100 if v >= 200 else 0, 50, "公克"
    labels = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    vals = [R.randint(3, 16) * 5 for _ in labels]
    return "圖書室每天的借書人數", "借書人數", labels, vals, 0, 10, "人"


def get():
    while True:
        d = data()
        if d and all((v - d[4]) % (d[5] if d[5] < 10 else d[5] // 2) == 0 for v in d[3]):
            return d


def s1(seen):
    def mk():
        title, what, labels, vals, lo, step, u = get()
        i = R.randrange(len(labels))
        v = vals[i]
        if (v - lo) % step:
            return None
        cells = (v - lo) // step
        tb = table(["時間"] + labels, [[what + "（" + u + "）"] + [str(x) for x in vals]])
        if lo:
            q = "把下表畫成折線圖，縱軸從 %d 開始（下面用 ≈ 省略），1 格代表 %d %s。%s的點要畫在從 %d 往上第幾格的線上？" % (lo, step, u, labels[i], lo) + tb
            w = [v // step, cells + 1, v - lo]
            e = "（%d － %d）÷ %d ＝ %d（格）。從 %d 開始數，不是從 0。" % (v, lo, step, cells, lo)
        else:
            q = "把下表畫成折線圖，1 格代表 %d %s。%s的點要畫在從 0 往上第幾格的線上？" % (step, u, labels[i]) + tb
            w = [v, cells + 1, cells - 1, v // 2]
            e = "%d ÷ %d ＝ %d（格）。" % (v, step, cells)
        return mcq(q, "第 %d 格" % cells, ["第 %d 格" % x for x in w if x != cells and x > 0], e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        title, what, labels, vals, lo, step, u = get()
        i = R.randrange(len(labels))
        drawn = vals[:]
        drawn[i] = vals[i] + R.choice([-1, 1]) * step
        if drawn[i] < lo or drawn[i] > lo + ((max(vals) - lo) // step + 1) * step:
            return None
        tb = table(["時間"] + labels, [[what + "（" + u + "）"] + [str(x) for x in vals]])
        q = "%s照下表畫了折線圖，有一個點畫錯了。是哪一個？" % NM.next() + tb + line_svg(title, labels, drawn, lo, step, u)
        return mcq(q, labels[i], [l for k, l in enumerate(labels) if k != i][:3] if i > 2 else [l for k, l in enumerate(labels) if k != i][-3:],
                   "表上%s是 %d %s，圖上卻畫在 %d，差了 1 格。" % (labels[i], vals[i], u, drawn[i]))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def scale():
        mx = R.choice([16, 28, 45, 70, 90, 140, 180, 260, 380, 450])
        q = "要畫折線圖，資料最大是 %d，縱軸最多只能畫 10 格。1 格代表多少最合適？" % mx
        opts = [1, 2, 5, 10, 20, 50]
        good = min(o for o in opts if mx / o <= 10)
        w = sorted([o for o in opts if o != good], key=lambda o: abs(opts.index(o) - opts.index(good)))[:3]
        return mcq(q, "1 格代表 %d" % good, ["1 格代表 %d" % o for o in w], "%d ÷ %d %s %d 格，不超過 10 格，又能畫得清楚。" % (mx, good, "＝" if mx % good == 0 else "≈", -(-mx // good)))

    def omit():
        lo = R.choice([130, 140, 30, 35, 20])
        rng = R.randint(4, 9)
        vals = sorted(R.sample(range(lo + 1, lo + rng + 2), 4))
        q = "資料是 %s，最小也有 %d。畫折線圖時，縱軸要怎麼畫，變化才看得清楚？" % ("、".join(map(str, vals)), vals[0])
        ans = "從 %d 開始，下面用 ≈ 省略" % lo
        return mcq(q, ans, ["從 0 開始，1 格代表 %d" % (lo // 2), "從 %d 開始，不用標示" % lo, "從 %d 開始，下面用 ≈ 省略" % (vals[-1] + 1)],
                   "資料都比 %d 大，把 0 到 %d 省略（畫 ≈），變化會比較明顯；起點要比最小的數小。" % (lo, lo))

    def steps():
        F = [("製作折線圖時，第一步要做什麼？", "整理資料，決定橫軸和縱軸", ["先把點連起來", "先畫長條", "先寫答案"], "先整理資料，決定橫軸（時間）和縱軸（數量），再定刻度、描點、連線。"),
             ("折線圖的橫軸通常放什麼？", "時間（日期、月份、年齡）", ["數量的刻度", "標題", "單位"], "折線圖看隨時間的變化，橫軸放時間。"),
             ("描好點之後要做什麼？", "依時間順序用線段把點連起來", ["從最低的點連到最高的點", "把點塗成長條", "把點擦掉"], "按照橫軸的順序，把相鄰的點用線段連起來。"),
             ("折線圖一定要寫上哪些東西？", "標題和單位", ["學生的名字", "價錢", "顏色說明"], "標題說明是什麼資料，單位說明數字代表什麼。")]
        return mcq(*R.choice(F))
    return pick_unique(R, scale, 8, seen) + pick_unique(R, omit, 8, seen) + pick_unique(R, steps, 4, seen)


def s4(seen):
    def mk():
        title, what, labels, vals, lo, step, u = get()
        g = line_svg(title, labels, vals, lo, step, u)
        diffs = [vals[k + 1] - vals[k] for k in range(len(vals) - 1)]
        kind = R.choice(["up", "down", "diff", "read"])
        if kind in ("up", "down"):
            m = max(diffs) if kind == "up" else min(diffs)
            if diffs.count(m) > 1 or (m <= 0 if kind == "up" else m >= 0):
                return None
            k = diffs.index(m)
            ans = "%s到%s" % (labels[k], labels[k + 1])
            w = ["%s到%s" % (labels[j], labels[j + 1]) for j in range(len(diffs)) if j != k]
            return mcq("看折線圖，%s在哪兩個時間之間%s得最多？" % (what, "增加" if kind == "up" else "減少") + g, ans, w,
                       "線往%s最陡的一段：%s，%s %d %s。" % ("上" if kind == "up" else "下", ans, "增加" if kind == "up" else "減少", abs(m), u))
        if kind == "diff":
            a, b = R.sample(range(len(labels)), 2)
            a, b = min(a, b), max(a, b)
            d = abs(vals[b] - vals[a])
            if d == 0:
                return None
            return mcq("看折線圖，%s和%s的%s相差多少%s？" % (labels[a], labels[b], what, u) + g, "%d %s" % (d, u),
                       ["%d %s" % (x, u) for x in (d + step, d - step if d > step else d + 2 * step, d // step if d // step != d else d + 1, vals[b]) if x != d and x > 0],
                       "%d － %d ＝ %d（%s）。" % (max(vals[a], vals[b]), min(vals[a], vals[b]), d, u))
        i = R.randrange(len(labels))
        v = vals[i]
        return mcq("看折線圖，%s的%s是多少？" % (labels[i], what) + g, "%d %s" % (v, u),
                   ["%d %s" % (x, u) for x in (v + step, v - step, (v - lo) // step if (v - lo) // step != v else v + 2 * step, v + step // 2 if step > 1 else v + 2) if x != v and x > 0],
                   "找到%s，對到左邊的刻度：%d %s（1 格是 %d）。" % (labels[i], v, u, step))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    SUIT = [("一年中每個月的平均氣溫", True), ("小樹每年長高的情形", True), ("一天中每小時的車流量", True), ("一週每天的體溫", True),
            ("班上同學最喜歡的運動", False), ("各班的人數", False), ("各種水果的價錢", False), ("全校各年級的近視人數", False)]

    def suit():
        it, ok = R.choice(SUIT)
        q = "「%s」最適合用哪一種圖表示？" % it
        if ok:
            return mcq(q, "折線圖", ["長條圖", "圓形圖", "地圖"], "這是隨時間變化的資料，用折線圖最能看出上升和下降。")
        return mcq(q, "長條圖", ["折線圖", "數線", "地圖"], "這是比較不同項目的多少，不是隨時間變化，用長條圖比較合適。")

    def trend():
        title, what, labels, vals, lo, step, u = get()
        if not all(vals[k + 1] > vals[k] for k in range(len(vals) - 1)):
            return None
        g = line_svg(title, labels, vals, lo, step, u)
        return mcq("看折線圖，%s的變化是怎樣？" % what + g, "一直增加", ["一直減少", "先增加後減少", "都沒有改變"], "折線一直往右上方走，表示一直增加。")

    def mount():
        title, what, labels, vals, lo, step, u = get()
        mx = max(vals)
        k = vals.index(mx)
        if vals.count(mx) > 1 or k in (0, len(vals) - 1) or not all(vals[j + 1] > vals[j] for j in range(k)) or not all(vals[j + 1] < vals[j] for j in range(k, len(vals) - 1)):
            return None
        g = line_svg(title, labels, vals, lo, step, u)
        return mcq("看折線圖，%s的變化是怎樣？" % what + g, "先增加，%s以後減少" % labels[k], ["一直增加", "一直減少", "先減少，%s以後增加" % labels[k]],
                   "折線先往右上走，到%s最高，之後往右下走。" % labels[k])
    return pick_unique(R, suit, 8, seen) + pick_unique(R, trend, 6, seen) + pick_unique(R, mount, 6, seen)


def tidy(items):
    f = lambda t: re.sub(r"([\u4e00-\u9fff])(\d)", r"\1 \2", t)
    for it in items:
        it["q"], it["e"] = f(it["q"]), f(it["e"])
        it["c"] = [f(c) for c in it["c"]]
    return items


def main():
    seen = set()
    sets = [("描點：畫在第幾格", s1(seen)), ("找出畫錯的點", s2(seen)), ("決定刻度和省略", s3(seen)),
            ("報讀折線圖", s4(seen)), ("看懂變化與選圖", s5(seen))]
    sets = [(t, tidy(it)) for t, it in sets]
    body = lesson(
        ["製作折線圖：<b>整理資料 → 定橫軸（時間）和縱軸 → 決定 1 格代表多少 → 描點 → 依序連線 → 寫標題和單位</b>。",
         "1 格的大小要讓最大的資料畫得下，也不要太擠。",
         "資料都很大、變化很小時，縱軸可以從接近最小值的數開始，下面用 <b>≈</b> 省略。"],
        [example("1 格代表 20 毫米，雨量 140 毫米畫在第幾格？", ["140 ÷ 20 ＝ 7。"], "第 7 格"),
         example("縱軸從 130 開始（≈ 省略），1 格代表 2 公分，身高 142 公分畫在第幾格？", ["（142 － 130）÷ 2 ＝ 6。"], "從 130 往上第 6 格")],
        [("1 格代表 20，卻把 140 畫在第 14 格", "要先除：140 ÷ 20 ＝ 7"),
         ("有 ≈ 省略時，從 0 開始數格子", "從縱軸的起點開始數"),
         ("把點從低連到高", "要照橫軸的時間順序連")])
    faq = [{"q": "折線圖怎麼畫？",
            "a": "先整理資料，橫軸放時間、縱軸放數量，決定 1 格代表多少，描點後依時間順序連線，最後寫上標題和單位。108課綱 D-5-1 要求五年級會製作生活中的折線圖。"},
           {"q": "折線圖上的 ≈ 是什麼意思？",
            "a": "表示縱軸下面的一段被省略了。資料都很大但變化很小時，省略後變化看得比較清楚。"},
           {"q": "什麼資料適合畫折線圖？",
            "a": "隨時間改變的資料，例如每月雨量、一天的氣溫、身高的成長；比較不同項目的多少則用長條圖。"}]
    make_unit(R, "grade-5", "making-line-graphs", "D-5-1",
              "製作折線圖：製作生活中的折線圖。",
              "製作折線圖",
              "五年級數學 折線圖 練習題｜描點・刻度・省略符號 學習單（附解答）",
              "製作折線圖",
              "國小五年級數學「製作折線圖」免費學習單：把表格畫成折線圖、描點畫在第幾格、決定 1 格代表多少和 ≈ 省略符號、找出畫錯的點、報讀變化與選擇合適的圖。100題線上練習馬上對答案，附可列印解答。",
              "描點 → 依時間順序連線",
              "先決定 1 格代表多少，再把每個點畫上去。",
              body, faq, sets, 27)


if __name__ == "__main__":
    main()
