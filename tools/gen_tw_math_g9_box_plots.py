# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：全距、四分位距與盒狀圖（108課綱 D-9-1）
  python3 tools/gen_tw_math_g9_box_plots.py
全距、中位數と第 1・第 3 四分位數（前半・後半の中位數）、四分位距 Q3 － Q1、盒狀圖を讀む（五數）、資料の割合（各區間 25%）、二組の比較。
資料の個數は 4 で割って 1 余る數を避ける（四分位數の決め方による違いが出ないように）。
誤答：全距を最大値だけにする、四分位距を Q3 ＋ Q1 にする、並べ替えずに中央を取る、盒の長さを全距とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fig, svg_wrap, text, line, INK, BLUE
from tw_g7 import tidy_sets

R = random.Random(81115)
NS = [7, 8, 10, 11, 12]
CTX = [("數學小考成績（分）", 30, 100), ("每天睡眠時間（小時）", 5, 10), ("一週閱讀時間（小時）", 0, 15), ("跳繩一分鐘次數（下）", 60, 160), ("身高（公分）", 145, 175), ("通勤時間（分鐘）", 5, 50)]


def med(xs):
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def quart(xs):
    xs = sorted(xs)
    n = len(xs)
    lo, hi = xs[:n // 2], xs[(n + 1) // 2:]
    return med(lo), med(xs), med(hi)


def g(v):
    return "%g" % v


def data():
    name, lo, hi = R.choice(CTX)
    n = R.choice(NS)
    xs = [R.randint(lo, hi) for _ in range(n)]
    return name, xs


def box(q, name, lo, hi, y0=34, label=True):
    mn, q1, m, q3, mx = q
    W = 340
    X = lambda v: 20 + (v - lo) / (hi - lo) * 300
    s = []
    if label:
        step = 5 if hi - lo <= 60 else 10 if hi - lo <= 120 else 20
        t = (lo // step) * step
        s.append(line(20, 70, 320, 70, INK, 1.2))
        while t <= hi:
            if t >= lo:
                s.append(line(X(t), 70, X(t), 75, INK, 1))
                s.append(text(X(t), 88, str(t), 10))
            t += step
    s.append(line(X(mn), y0, X(q1), y0, INK, 1.6))
    s.append(line(X(q3), y0, X(mx), y0, INK, 1.6))
    s.append(line(X(mn), y0 - 8, X(mn), y0 + 8, INK, 1.6))
    s.append(line(X(mx), y0 - 8, X(mx), y0 + 8, INK, 1.6))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='24' fill='#e3eefb' stroke='%s' stroke-width='1.6'/>" % (X(q1), y0 - 12, X(q3) - X(q1), BLUE))
    s.append(line(X(m), y0 - 12, X(m), y0 + 12, BLUE, 2.4))
    return s


def boxfig(q, name):
    lo = int(q[0]) - (int(q[0]) % 5)
    hi = int(q[4]) + (5 - int(q[4]) % 5) % 5
    if hi == lo:
        hi += 5
    s = box(q, name, lo, hi, y0=44)
    X = lambda v: 20 + (v - lo) / (hi - lo) * 300
    s = [x.replace("y1='70'", "y1='80'").replace("y2='70'", "y2='80'").replace("y1='75'", "y1='85'").replace("y2='75'", "y2='85'").replace("y='88'", "y='98'") for x in s]
    for v in q:
        s.append(text(X(v), 26, g(v), 11, col=BLUE))
    s.append(text(170, 12, name, 12))
    return fig(svg_wrap(340, 106, "".join(s), name + "盒狀圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def show(xs):
    return "，".join(str(x) for x in xs)


def s1(seen):
    def mk():
        name, xs = data()
        r = max(xs) - min(xs)
        if r == 0:
            return None
        q = "下面是 %d 位學生的%s：<br>%s<br>全距是多少？" % (len(xs), name, show(xs))
        return mcq(q, str(r), [str(max(xs)), str(xs[-1] - xs[0]) if xs[-1] - xs[0] != r else str(r + 1), str(max(xs) + min(xs))], "全距 ＝ 最大值 － 最小值 ＝ %d － %d ＝ %d。" % (max(xs), min(xs), r))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        name, xs = data()
        s_ = sorted(xs)
        q1, m, q3 = quart(xs)
        k = R.choice(["Q1", "Q3", "Q2"])
        v = {"Q1": q1, "Q2": m, "Q3": q3}[k]
        nm = {"Q1": "第 1 四分位數 Q<sub>1</sub> ", "Q2": "中位數（第 2 四分位數）", "Q3": "第 3 四分位數 Q<sub>3</sub> "}[k]
        q = "下面是 %d 筆%s：<br>%s<br>%s是多少？" % (len(xs), name, show(xs), nm)
        unsorted = med(xs) if k == "Q2" else (med(xs[:len(xs) // 2]) if k == "Q1" else med(xs[(len(xs) + 1) // 2:]))
        w = [g(x) for x in ({"Q1": m, "Q2": q1, "Q3": m}[k], unsorted, {"Q1": q3, "Q2": q3, "Q3": q1}[k], v + 1) if x != v]
        lo = s_[:len(s_) // 2]
        hi = s_[(len(s_) + 1) // 2:]
        e = "先由小到大排：%s。" % show(s_)
        e += {"Q1": "前半部 %s 的中位數是 %s。" % (show(lo), g(q1)), "Q2": "中間的數是 %s。" % g(m), "Q3": "後半部 %s 的中位數是 %s。" % (show(hi), g(q3))}[k]
        return mcq(q, g(v), w, e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        name, xs = data()
        q1, m, q3 = quart(xs)
        v = q3 - q1
        if v <= 0:
            return None
        q = "下面是 %d 筆%s：<br>%s<br>四分位距是多少？" % (len(xs), name, show(xs))
        return mcq(q, g(v), [g(x) for x in (q3 + q1, max(xs) - min(xs), q3 - m if q3 - m != v else v + 1) if x != v], "排序後 Q<sub>1</sub> ＝ %s，Q<sub>3</sub> ＝ %s，四分位距 ＝ Q<sub>3</sub> － Q<sub>1</sub> ＝ %s。" % (g(q1), g(q3), g(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        name, xs = data()
        s_ = sorted(xs)
        q1, m, q3 = quart(xs)
        five = (s_[0], q1, m, q3, s_[-1])
        if len(set(five)) < 5 or any(v % 1 for v in five):
            return None
        span = five[4] - five[0]
        if min(b - a for a, b in zip(five, five[1:])) < span * 0.1:
            return None
        bf = boxfig(five, name)
        k = R.choice(["IQR", "range", "Q1", "med", "pct"])
        if k == "IQR":
            q = "看盒狀圖，四分位距是多少？" + bf
            v, w, e = q3 - q1, [s_[-1] - s_[0], q3, m - q1], "盒子的兩端是 Q<sub>1</sub> ＝ %s、Q<sub>3</sub> ＝ %s，四分位距 ＝ %s。" % (g(q1), g(q3), g(q3 - q1))
        elif k == "range":
            q = "看盒狀圖，全距是多少？" + bf
            v, w, e = s_[-1] - s_[0], [q3 - q1, s_[-1], q3 - s_[0]], "兩條鬚的端點是最小值 %d、最大值 %d，全距 ＝ %d。" % (s_[0], s_[-1], s_[-1] - s_[0])
        elif k == "Q1":
            q = "看盒狀圖，第 1 四分位數是多少？" + bf
            v, w, e = q1, [s_[0], m, q3], "盒子的左端是 Q<sub>1</sub> ＝ %s。" % g(q1)
        elif k == "med":
            q = "看盒狀圖，中位數是多少？" + bf
            v, w, e = m, [(s_[0] + s_[-1]) / 2 if (s_[0] + s_[-1]) / 2 != m else m + 1, q1, q3], "盒子中間的直線是中位數 %s。" % g(m)
            v = m
        else:
            q = "看盒狀圖，大約有百分之幾的資料在 %s 到 %s 之間？" % (g(q1), g(q3)) + bf
            return mcq(q, "50%", ["25%", "75%", "100%"], "盒子從 Q<sub>1</sub> 到 Q<sub>3</sub>，包含中間大約 50% 的資料。")
        return mcq(q, g(v), [g(x) for x in w if x != v] + [g(v + 2)], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def cmp():
        lo, hi = 40, 100
        a = sorted(R.sample(range(lo, hi + 1), 5))
        b = sorted(R.sample(range(lo, hi + 1), 5))
        if len(set(a)) < 5 or len(set(b)) < 5 or a[2] == b[2] or (a[3] - a[1]) == (b[3] - b[1]):
            return None
        s = box(a, "", lo, hi, 26, True)
        s += box(b, "", lo, hi, 52, False)
        s = [x.replace("y1='70'", "y1='80'").replace("y2='70'", "y2='80'") for x in s]
        s.append(text(4, 30, "甲", 12, "start"))
        s.append(text(4, 56, "乙", 12, "start"))
        svg = fig(svg_wrap(340, 96, "".join(s), "甲乙兩班成績盒狀圖").replace("<svg ", "<svg data-pf='lg' ", 1))
        k = R.choice(["med", "iqr"])
        if k == "med":
            ans = "甲" if a[2] > b[2] else "乙"
            q = "甲、乙兩班數學成績的盒狀圖如下，哪一班的中位數比較高？" + svg
            return mcq(q, "%s班" % ans, ["%s班" % ("乙" if ans == "甲" else "甲"), "一樣高", "不能判斷"], "比較盒子中間的線：甲 %d、乙 %d，%s班比較高。" % (a[2], b[2], ans))
        ans = "甲" if a[3] - a[1] > b[3] - b[1] else "乙"
        q = "甲、乙兩班數學成績的盒狀圖如下，哪一班中間 50% 的成績比較分散（四分位距比較大）？" + svg
        return mcq(q, "%s班" % ans, ["%s班" % ("乙" if ans == "甲" else "甲"), "一樣分散", "不能判斷"], "比較盒子的長度：甲 %d － %d ＝ %d，乙 %d － %d ＝ %d，%s班比較大。" % (a[3], a[1], a[3] - a[1], b[3], b[1], b[3] - b[1], ans))

    def pct():
        n = R.choice([20, 40, 100, 200])
        k = R.choice(["above", "below", "box"])
        nm = {"above": "大於第 3 四分位數", "below": "小於第 1 四分位數", "box": "在 Q<sub>1</sub> 和 Q<sub>3</sub> 之間"}[k]
        v = n // 4 if k != "box" else n // 2
        q = "%d 筆資料（沒有重複的數），%s的大約有幾筆？" % (n, nm)
        return mcq(q, "%d 筆" % v, ["%d 筆" % x for x in (n // 2 if k != "box" else n // 4, n * 3 // 4, n // 3 if n % 3 == 0 else n // 5)], "四分位數把資料分成 4 等份，每份約 25%%：%s約 %d%%，%d 筆的 %d%% 約 %d 筆。" % (nm, 25 if k != "box" else 50, n, 25 if k != "box" else 50, v))
    return pick_unique(R, cmp, 14, seen) + pick_unique(R, pct, 6, seen)


def main():
    seen = set()
    sets = [("全距", s1(seen)), ("四分位數", s2(seen)), ("四分位距", s3(seen)),
            ("讀盒狀圖", s4(seen)), ("比較與解讀", s5(seen))]
    tidy_sets(sets)
    demo = boxfig((52, 64, 72, 85, 96), "數學小考成績（分）")
    body = lesson(
        ["<b>全距</b> ＝ 最大值 － 最小值，表示資料分布的範圍。",
         "資料由小到大排好，<b>中位數</b>把資料分成前後兩半；前半部的中位數是 <b>Q<sub>1</sub></b>，後半部的中位數是 <b>Q<sub>3</sub></b>（資料個數是奇數時，中位數本身不放進前後半部）。",
         "<b>四分位距 ＝ Q<sub>3</sub> － Q<sub>1</sub></b>，是中間 50% 資料的範圍。",
         "<b>盒狀圖</b>用五個數畫成：最小值、Q<sub>1</sub>、中位數、Q<sub>3</sub>、最大值。" + demo],
        [example("3，5，6，8，9，10，12，15 的四分位數", ["前半 3，5，6，8：Q<sub>1</sub> ＝ 5.5。", "後半 9，10，12，15：Q<sub>3</sub> ＝ 11。"], "Q<sub>1</sub> ＝ 5.5，Q<sub>3</sub> ＝ 11，四分位距 5.5"),
         example("上面的盒狀圖，四分位距？", ["85 － 64。"], "21")],
        [("沒排序就找中間的數", "一定要先由小到大排"),
         ("四分位距 ＝ Q<sub>3</sub> ＋ Q<sub>1</sub>", "是相減：Q<sub>3</sub> － Q<sub>1</sub>"),
         ("盒子的長度就是全距", "盒子是四分位距；全距是兩條鬚的端點相減")])
    faq = [{"q": "四分位距和全距有什麼不同？",
            "a": "全距看全部資料的範圍，容易受極端值影響；四分位距只看中間 50% 的資料，比較不受特別大或特別小的數影響。"},
           {"q": "盒狀圖怎麼看資料是否集中？",
            "a": "盒子越短，中間 50% 的資料越集中；鬚越長，兩端的資料越分散。"},
           {"q": "九年級的統計要學什麼？",
            "a": "108課綱 D-9-1：統計數據的分布，包含全距、四分位距和盒狀圖。"}]
    make_unit(R, "grade-9", "box-plots", "D-9-1",
              "統計數據的分布：全距；四分位距；盒狀圖。",
              "全距、四分位距與盒狀圖",
              "九年級數學 盒狀圖 練習題｜全距・四分位數・四分位距 學習單（附解答）",
              "盒狀圖與四分位距",
              "國中九年級數學「全距、四分位距與盒狀圖」免費學習單：全距、第 1 和第 3 四分位數、四分位距、讀盒狀圖的五個數、比較兩班成績的盒狀圖。100題線上練習馬上對答案，附可列印解答。",
              "四分位距 ＝ Q<sub>3</sub> － Q<sub>1</sub>",
              "盒狀圖：最小值、Q<sub>1</sub>、中位數、Q<sub>3</sub>、最大值。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
