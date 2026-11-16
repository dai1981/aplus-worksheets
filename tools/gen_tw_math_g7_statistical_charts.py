# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：統計圖表（108課綱 D-7-1）
  python3 tools/gen_tw_math_g7_statistical_charts.py
次數分配表（組距・組界）、直方圖を讀む、相對次數（百分率）、累積次數、列聯表（二つの分類）、圖表の選び方。
誤答：組界の上限を含める、相對次數を總數で割らない、累積次數を各組の次數と取り違える、列聯表で行と列を取り違える。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, fig, svg_wrap, text, line, INK, num
from tw_g7 import tidy_sets

R = random.Random(71025)
NM = Names(R)
CTX = [("數學成績", "分", 40, 10), ("身高", "公分", 140, 5), ("每週運動時間", "小時", 0, 2), ("一分鐘跳繩次數", "下", 60, 20), ("體重", "公斤", 35, 5)]


def data():
    name, u, lo, w = R.choice(CTX)
    k = R.choice([5, 6])
    fs = [R.randint(1, 12) for _ in range(k)]
    if sum(fs) not in range(20, 61):
        return None
    return name, u, lo, w, fs


def bounds(lo, w, k):
    return [(lo + i * w, lo + (i + 1) * w) for i in range(k)]


def hist(name, u, lo, w, fs):
    k = len(fs)
    mx = max(fs)
    top = (mx // 2 + 1) * 2
    W, H = 60 + k * 46, 210
    s = [text(W / 2, 14, "%s直方圖" % name, 13)]
    X0, Y0, ph = 40, 180, 150
    for t in range(0, top + 1, 2):
        y = Y0 - ph * t / top
        s.append(line(X0, y, X0 + k * 46, y, "#e2e2e2" if t else INK, 1))
        s.append(text(X0 - 6, y + 4, str(t), 10, anchor="end"))
    for i, f in enumerate(fs):
        x = X0 + i * 46
        h = ph * f / top
        s.append("<rect x='%d' y='%.1f' width='46' height='%.1f' fill='#bfe0c6' stroke='#2e7d4f' stroke-width='1.2'/>" % (x, Y0 - h, h))
    for i in range(k + 1):
        s.append(text(X0 + i * 46, Y0 + 14, str(lo + i * w), 10))
    s.append(text(X0 + k * 46 + 4, Y0 + 14, "（%s）" % u, 10, anchor="start"))
    s.append(text(X0 - 22, 26, "人數", 10))
    return fig(svg_wrap(W + 30, H, "".join(s), name + "直方圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def s1(seen):
    def mk():
        d = data()
        if not d:
            return None
        name, u, lo, w, fs = d
        bs = bounds(lo, w, len(fs))
        i = R.randrange(len(fs))
        g = hist(name, u, lo, w, fs)
        kind = R.choice(["n", "tot", "max"])
        if kind == "n":
            q = "看直方圖，%s在 %d～%d %s的有幾人？（含 %d，不含 %d）" % (name, bs[i][0], bs[i][1], u, bs[i][0], bs[i][1]) + g
            return mcq(q, "%d 人" % fs[i], ["%d 人" % x for x in (fs[i] + 1, fs[i - 1] if i and fs[i - 1] != fs[i] else fs[i] + 2, sum(fs[:i + 1]) if sum(fs[:i + 1]) != fs[i] else fs[i] + 3)], "找到 %d～%d 這一組的長條，高度是 %d。" % (bs[i][0], bs[i][1], fs[i]))
        if kind == "tot":
            q = "看直方圖，一共有幾人？" + g
            t = sum(fs)
            return mcq(q, "%d 人" % t, ["%d 人" % x for x in (max(fs), len(fs), t - fs[0])], "把每一組的人數加起來：%s ＝ %d。" % (" ＋ ".join(map(str, fs)), t))
        m = max(fs)
        if fs.count(m) > 1:
            return None
        j = fs.index(m)
        q = "看直方圖，哪一組的人數最多？" + g
        ans = "%d～%d %s" % (bs[j][0], bs[j][1], u)
        return mcq(q, ans, ["%d～%d %s" % (a, b, u) for a, b in bs if (a, b) != bs[j]][:3], "最高的長條是 %s，有 %d 人。" % (ans, m))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        d = data()
        if not d:
            return None
        name, u, lo, w, fs = d
        bs = bounds(lo, w, len(fs))
        tb = table(["%s（%s）" % (name, u)] + ["%d～%d" % b for b in bs], [["人數"] + [str(f) for f in fs]])
        t = sum(fs)
        i = R.randrange(len(fs))
        rel = F(fs[i] * 100, t)
        if rel.denominator != 1:
            return None
        q = "下表中，%d～%d 這一組的相對次數是百分之幾？" % bs[i] + tb
        return mcq(q, "%d%%" % rel, ["%d%%" % x for x in (fs[i], 100 - rel, rel + 5)  if x != rel], "相對次數 ＝ 該組次數 ÷ 總次數：%d ÷ %d ＝ %d%%。" % (fs[i], t, rel))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        d = data()
        if not d:
            return None
        name, u, lo, w, fs = d
        bs = bounds(lo, w, len(fs))
        tb = table(["%s（%s）" % (name, u)] + ["%d～%d" % b for b in bs], [["人數"] + [str(f) for f in fs]])
        i = R.randrange(1, len(fs))
        cum = sum(fs[:i + 1])
        q = "下表中，%s未滿 %d %s的有幾人？（累積次數）" % (name, bs[i][1], u) + tb
        return mcq(q, "%d 人" % cum, ["%d 人" % x for x in (fs[i], sum(fs[:i]), sum(fs) - cum)  if x != cum and x > 0] + ["%d 人" % (cum + 1)], "從第一組加到 %d～%d 這一組：%s ＝ %d。" % (bs[i][0], bs[i][1], " ＋ ".join(map(str, fs[:i + 1])), cum))

    def bound():
        name, u, lo, w = R.choice(CTX)[:4]
        v = lo + w * R.randint(1, 4)
        q = "組距是 %d、第一組是 %d～%d 的次數分配表中，%s正好是 %d %s的人要記在哪一組？" % (w, lo, lo + w, name, v, u)
        ans = "%d～%d" % (v, v + w)
        return mcq(q, ans, ["%d～%d" % (v - w, v), "兩組都記", "不用記"], "每一組包含下限、不包含上限，%d 要記在 %d～%d。" % (v, v, v + w))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, bound, 6, seen)


def s4(seen):
    def mk():
        a, b, c, d = [R.randint(3, 25) for _ in range(4)]
        rows = R.choice([("男生", "女生"), ("七年級", "八年級"), ("走路", "搭車")])
        cols = R.choice([("喜歡", "不喜歡"), ("有戴眼鏡", "沒戴眼鏡"), ("參加社團", "沒參加社團")])
        tb = table(["", cols[0], cols[1], "合計"], [[rows[0], str(a), str(b), str(a + b)], [rows[1], str(c), str(d), str(c + d)], ["合計", str(a + c), str(b + d), str(a + b + c + d)]])
        kind = R.choice(["cell", "col", "pct"])
        if kind == "cell":
            q = "下表是列聯表。%s中%s的有幾人？" % (rows[1], cols[0]) + tb
            return mcq(q, "%d 人" % c, ["%d 人" % x for x in (a, d, a + c)  if x != c] + ["%d 人" % (c + d)], "找「%s」那一列和「%s」那一行交叉的格子：%d。" % (rows[1], cols[0], c))
        if kind == "col":
            q = "下表是列聯表。%s的一共有幾人？" % cols[1] + tb
            return mcq(q, "%d 人" % (b + d), ["%d 人" % x for x in (b, c + d, a + b)  if x != b + d] + ["%d 人" % (b + d + 1)], "%s那一行加起來：%d ＋ %d ＝ %d。" % (cols[1], b, d, b + d))
        p = F(a * 100, a + b)
        if p.denominator != 1:
            return None
        q = "下表是列聯表。%s中%s的占百分之幾？" % (rows[0], cols[0]) + tb
        return mcq(q, "%d%%" % p, ["%d%%" % x for x in (F(a * 100, a + c) if F(a * 100, a + c).denominator == 1 else p + 10, 100 - p, a)  if x != p], "%s共 %d 人，其中%s %d 人：%d ÷ %d ＝ %d%%。" % (rows[0], a + b, cols[0], a, a, a + b, p))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    F_ = [("要看全班數學成績在各分數區間的人數分布，最適合用哪一種圖？", "直方圖", ["圓形圖", "折線圖", "列聯表"], "連續的數值分組統計，用直方圖。"),
          ("要看一年中每個月的氣溫變化，最適合用哪一種圖？", "折線圖", ["直方圖", "圓形圖", "列聯表"], "隨時間的變化用折線圖。"),
          ("要看各種交通方式占全校學生的比例，最適合用哪一種圖？", "圓形圖", ["直方圖", "折線圖", "長條圖"], "看部分占全體的比例用圓形圖。"),
          ("要同時看「性別」和「是否戴眼鏡」兩種分類的人數，最適合用什麼？", "列聯表", ["折線圖", "圓形圖", "直方圖"], "兩種分類交叉統計用列聯表。"),
          ("要比較各班的捐書數量，最適合用哪一種圖？", "長條圖", ["折線圖", "直方圖", "列聯表"], "比較不同項目的數量用長條圖。"),
          ("直方圖和長條圖最大的不同是什麼？", "直方圖的長條相連，表示連續的數值分組", ["直方圖一定是橫的", "長條圖不能比較大小", "直方圖不用標單位"], "直方圖的橫軸是連續的組界，長條之間沒有空隙。"),
          ("次數分配表中所有相對次數加起來是多少？", "100%", ["50%", "不一定", "總人數"], "每一組占全體的比例，合起來是全體。"),
          ("累積次數分配表中，最後一組的累積次數等於什麼？", "總次數", ["最後一組的次數", "0", "最大的次數"], "從第一組加到最後一組，就是全部。")]
    out = [mcq(*f) for f in F_]
    for o in out:
        seen.add(o["q"])

    def miss():
        d = data()
        if not d:
            return None
        name, u, lo, w, fs = d
        bs = bounds(lo, w, len(fs))
        t = sum(fs)
        i = R.randrange(len(fs))
        tb = table(["%s（%s）" % (name, u)] + ["%d～%d" % b for b in bs], [["人數"] + ["？" if j == i else str(f) for j, f in enumerate(fs)]])
        q = "總共 %d 人，表中「？」是多少？" % t + tb
        return mcq(q, "%d 人" % fs[i], ["%d 人" % x for x in (fs[i] + 1, fs[i] - 1 if fs[i] > 1 else fs[i] + 2, t - fs[i])  if x != fs[i]], "%d －（其他各組的和 %d）＝ %d。" % (t, t - fs[i], fs[i]))
    return out + pick_unique(R, miss, 12, seen)


def main():
    seen = set()
    sets = [("讀直方圖", s1(seen)), ("相對次數", s2(seen)), ("累積次數與組界", s3(seen)),
            ("列聯表", s4(seen)), ("選擇圖表與綜合", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>次數分配表</b>：把資料按<b>組距</b>分組，每組包含下限、不包含上限（例如 60～70 含 60 不含 70）。",
         "<b>直方圖</b>：把次數分配表畫成長條相連的圖，橫軸是組界，縱軸是次數。",
         "<b>相對次數</b> ＝ 該組次數 ÷ 總次數（常用百分率）；<b>累積次數</b>：從第一組一直加到該組。",
         "<b>列聯表</b>：同時用兩種分類（例如性別、是否戴眼鏡）交叉統計人數。"],
        [example("40 人中 60～70 分有 10 人，相對次數？", ["10 ÷ 40 ＝ 0.25。"], "25%"),
         example("各組人數 3、5、8，第三組的累積次數？", ["3 ＋ 5 ＋ 8。"], "16")],
        [("70 分記在 60～70 這一組", "不含上限，記在 70～80"),
         ("相對次數直接寫次數", "要除以總次數"),
         ("累積次數只寫該組的次數", "要從第一組加到該組")])
    faq = [{"q": "直方圖和長條圖有什麼不同？",
            "a": "直方圖的橫軸是連續的數值分組，長條相連沒有空隙；長條圖比較的是不同項目，長條之間有空隙。"},
           {"q": "什麼是列聯表？",
            "a": "同時按兩種分類統計的表格，例如列是男生、女生，行是有沒有戴眼鏡，可以看出兩種分類之間的關係。"},
           {"q": "七年級的統計圖表要學什麼？",
            "a": "108課綱 D-7-1：蒐集生活中的數據，整理並繪製成直方圖、長條圖、圓形圖、折線圖和列聯表。"}]
    make_unit(R, "grade-7", "statistical-charts", "D-7-1",
              "統計圖表：蒐集生活中常見的數據資料，整理並繪製成含有原始資料或百分率的統計圖表：直方圖、長條圖、圓形圖、折線圖、列聯表。遇到複雜數據時可使用計算機輔助，教師可使用電腦應用軟體演示教授。",
              "統計圖表：直方圖、相對次數、列聯表",
              "七年級數學 統計圖表 練習題｜直方圖・相對次數・累積次數・列聯表 學習單（附解答）",
              "統計圖表",
              "國中七年級數學「統計圖表」免費學習單：讀直方圖、相對次數百分率、累積次數和組界、列聯表，以及選擇合適的統計圖表。100題線上練習馬上對答案，附可列印解答。",
              "相對次數 ＝ 該組次數 ÷ 總次數",
              "每一組包含下限、不包含上限。",
              body, faq, sets, 25)


if __name__ == "__main__":
    main()
