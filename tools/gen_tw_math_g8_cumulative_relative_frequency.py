# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：累積次數與累積相對次數（108課綱 D-8-1）
  python3 tools/gen_tw_math_g8_cumulative_relative_frequency.py
次數分配表から累積次數・相對次數・累積相對次數を求める、累積相對次數折線圖を讀む、「以上」を 100% から引く、人數に戻す。
誤答：累積を各組の次數と取り違える、累積を一つ前の組までにする、「以上」で 100% から引かない、總數で割らない。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, table, fig, svg_wrap, text, line, INK
from tw_g7 import tidy_sets

R = random.Random(81013)
CTX = [("數學成績", "分", 40, 10), ("身高", "公分", 140, 5), ("每週運動時間", "小時", 0, 2), ("一分鐘跳繩次數", "下", 60, 20), ("上學通勤時間", "分鐘", 0, 10)]


def data():
    name, u, lo, w = R.choice(CTX)
    N = R.choice([20, 25, 50])
    k = 5
    while True:
        cut = sorted(R.sample(range(1, N), k - 1))
        fs = [b - a for a, b in zip([0] + cut, cut + [N])]
        if min(fs) >= 1 and max(fs) <= N * 0.45:
            break
    return name, u, lo, w, fs, N


def pct(n, N):
    return n * 100 // N


def tb(name, u, lo, w, fs):
    return table(["%s（%s）" % (name, u)] + ["%d～%d" % (lo + i * w, lo + (i + 1) * w) for i in range(len(fs))], [["人數"] + [str(f) for f in fs]])


def chart(name, u, lo, w, fs, N):
    k = len(fs)
    cs = [0]
    for f in fs:
        cs.append(cs[-1] + f)
    X0, Y0, ph, cw = 46, 196, 160, 52
    W = X0 + k * cw + 60
    s = [text(W / 2, 14, "%s累積相對次數折線圖" % name, 13)]
    for t in range(0, 101, 20):
        y = Y0 - ph * t / 100
        s.append(line(X0, y, X0 + k * cw, y, "#e2e2e2" if t else INK, 1))
        s.append(text(X0 - 6, y + 4, "%d" % t, 10, anchor="end"))
    for i in range(k + 1):
        x = X0 + i * cw
        s.append(line(x, Y0, x, Y0 - ph, "#eeeeee", 1))
        s.append(text(x, Y0 + 14, str(lo + i * w), 10))
    pts = [(X0 + i * cw, Y0 - ph * c / N) for i, c in enumerate(cs)]
    s.append("<polyline points='%s' fill='none' stroke='#2e7d4f' stroke-width='2.2'/>" % " ".join("%.1f,%.1f" % p for p in pts))
    for i, (x, y) in enumerate(pts):
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='#2e7d4f'/>" % (x, y))
        if i:
            s.append(text(x - 4, y - 7, "%d" % pct(cs[i], N), 10, anchor="end", col="#2e7d4f"))
    s.append(text(X0 + k * cw + 4, Y0 + 14, "（%s）" % u, 10, anchor="start"))
    s.append(text(X0 - 20, 30, "（%）", 10))
    return fig(svg_wrap(W, 216, "".join(s), name + "累積相對次數折線圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def cum(fs, i):
    return sum(fs[:i + 1])


def s1(seen):
    def mk():
        name, u, lo, w, fs, N = data()
        i = R.randint(1, 4)
        hi = lo + (i + 1) * w
        c = cum(fs, i)
        q = "%s 位學生的%s如下表，未滿 %d %s的累積次數是多少？" % (N, name, hi, u) + tb(name, u, lo, w, fs)
        return mcq(q, "%d 人" % c, ["%d 人" % x for x in (fs[i], cum(fs, i - 1), N - c, c + fs[i + 1] if i < 4 else c - 1)],
                   "累積次數是從第一組加到這一組：%s ＝ %d（人）。" % (" ＋ ".join(map(str, fs[:i + 1])), c))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def rel():
        name, u, lo, w, fs, N = data()
        i = R.randint(0, 4)
        a, b = lo + i * w, lo + (i + 1) * w
        q = "%s 位學生的%s如下表，%d～%d %s這一組的相對次數是多少？" % (N, name, a, b, u) + tb(name, u, lo, w, fs)
        p = pct(fs[i], N)
        return mcq(q, "%d%%" % p, ["%d%%" % x for x in (fs[i], pct(cum(fs, i), N), 100 - p, p + (100 // N))],
                   "相對次數 ＝ 該組次數 ÷ 總次數：%d ÷ %d ＝ %d%%。" % (fs[i], N, p))

    def crel():
        name, u, lo, w, fs, N = data()
        i = R.randint(1, 3)
        hi = lo + (i + 1) * w
        c = cum(fs, i)
        p = pct(c, N)
        q = "%s 位學生的%s如下表，未滿 %d %s的累積相對次數是多少？" % (N, name, hi, u) + tb(name, u, lo, w, fs)
        return mcq(q, "%d%%" % p, ["%d%%" % x for x in (pct(fs[i], N), c, 100 - p, pct(cum(fs, i - 1), N))],
                   "累積次數 %s ＝ %d，%d ÷ %d ＝ %d%%。" % (" ＋ ".join(map(str, fs[:i + 1])), c, c, N, p))
    return pick_unique(R, rel, 8, seen) + pick_unique(R, crel, 12, seen)


def s3(seen):
    def mk():
        name, u, lo, w, fs, N = data()
        i = R.randint(1, 4)
        x = lo + i * w
        c = cum(fs, i - 1)
        p = 100 - pct(c, N)
        q = "%s 位學生的%s如下表，%d %s以上的人占全部的百分之幾？" % (N, name, x, u) + tb(name, u, lo, w, fs)
        return mcq(q, "%d%%" % p, ["%d%%" % v for v in (pct(c, N), pct(fs[i], N), 100 - pct(cum(fs, i), N), N - c)],
                   "未滿 %d 的累積相對次數是 %d ÷ %d ＝ %d%%，以上的占 100%% － %d%% ＝ %d%%。" % (x, c, N, pct(c, N), pct(c, N), p))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        name, u, lo, w, fs, N = data()
        g = chart(name, u, lo, w, fs, N)
        k = R.choice(["below", "group", "above"])
        if k == "below":
            i = R.randint(0, 3)
            hi = lo + (i + 1) * w
            p = pct(cum(fs, i), N)
            q = "看累積相對次數折線圖，%s未滿 %d %s的占百分之幾？" % (name, hi, u) + g
            return mcq(q, "%d%%" % p, ["%d%%" % v for v in (pct(fs[i], N), 100 - p, pct(cum(fs, i + 1), N), pct(cum(fs, i - 1), N) if i else p + 5)],
                       "找橫軸 %d 的點，縱軸讀到 %d%%。" % (hi, p))
        if k == "group":
            i = R.randint(1, 4)
            a, b = lo + i * w, lo + (i + 1) * w
            p1, p2 = pct(cum(fs, i - 1), N), pct(cum(fs, i), N)
            q = "看累積相對次數折線圖，%s在 %d～%d %s這一組的相對次數是多少？" % (name, a, b, u) + g
            return mcq(q, "%d%%" % (p2 - p1), ["%d%%" % v for v in (p2, p1, 100 - p2, p2 - p1 + 10)],
                       "這一組的相對次數 ＝ 兩點的差：%d%% － %d%% ＝ %d%%。" % (p2, p1, p2 - p1))
        i = R.randint(1, 4)
        x = lo + i * w
        p = pct(cum(fs, i - 1), N)
        q = "看累積相對次數折線圖，%s在 %d %s以上的占百分之幾？" % (name, x, u) + g
        return mcq(q, "%d%%" % (100 - p), ["%d%%" % v for v in (p, pct(fs[i], N), 100 - pct(cum(fs, i), N))],
                   "未滿 %d 的占 %d%%，以上的占 100%% － %d%% ＝ %d%%。" % (x, p, p, 100 - p))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def count():
        name, u, lo, w, fs, N = data()
        g = chart(name, u, lo, w, fs, N)
        i = R.randint(1, 4)
        a, b = lo + i * w, lo + (i + 1) * w
        p = pct(fs[i], N)
        q = "調查 %d 位學生，看下面的累積相對次數折線圖，%s在 %d～%d %s的有幾人？" % (N, name, a, b, u) + g
        return mcq(q, "%d 人" % fs[i], ["%d 人" % v for v in (cum(fs, i), p, N - cum(fs, i), fs[i] + 1)],
                   "相對次數 %d%% － %d%% ＝ %d%%，%d × %d%% ＝ %d（人）。" % (pct(cum(fs, i), N), pct(cum(fs, i - 1), N), p, N, p, fs[i]))

    def missing():
        name, u, lo, w, fs, N = data()
        i = R.randint(0, 4)
        shown = [str(f) if j != i else "？" for j, f in enumerate(fs)]
        t = table(["%s（%s）" % (name, u)] + ["%d～%d" % (lo + j * w, lo + (j + 1) * w) for j in range(5)], [["人數"] + shown])
        q = "%d 位學生的%s如下表，有一組的人數看不清楚。這一組的相對次數是多少？" % (N, name) + t
        p = pct(fs[i], N)
        return mcq(q, "%d%%" % p, ["%d%%" % v for v in (fs[i], 100 - p, p + 100 // N * 2)],
                   "這一組有 %d － %d ＝ %d 人，%d ÷ %d ＝ %d%%。" % (N, N - fs[i], fs[i], fs[i], N, p))
    return pick_unique(R, count, 12, seen) + pick_unique(R, missing, 8, seen)


def main():
    seen = set()
    sets = [("累積次數", s1(seen)), ("相對次數與累積相對次數", s2(seen)), ("「以上」的百分比", s3(seen)),
            ("讀累積相對次數折線圖", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    demo_fs = [2, 4, 8, 4, 2]
    body = lesson(
        ["<b>累積次數</b>：從第一組加到這一組的次數，表示「未滿這組上限」的有多少。",
         "<b>相對次數</b> ＝ 該組次數 ÷ 總次數；<b>累積相對次數</b> ＝ 累積次數 ÷ 總次數，最後一組一定是 100%。",
         "<b>累積相對次數折線圖</b>：每組上限畫一個點，連成一條往上的折線。兩點相減就是這一組的相對次數。",
         "「○○ 以上」的百分比 ＝ 100% － 未滿 ○○ 的累積相對次數。"],
        [example("20 位學生的數學成績如下表，未滿 70 分的累積相對次數？" + tb("數學成績", "分", 40, 10, demo_fs), ["累積次數 2 ＋ 4 ＋ 8 ＝ 14。", "14 ÷ 20 ＝ 70%。"], "70%"),
         example("同一份資料，70 分以上的占多少？", ["100% － 70% ＝ 30%。"], "30%")],
        [("把這一組的次數當成累積次數", "累積要從第一組一直加到這一組"),
         ("「70 分以上」直接讀 70 的點", "讀到的是未滿 70，要用 100% 去減"),
         ("相對次數忘了除以總數", "相對次數 ＝ 次數 ÷ 總次數")])
    faq = [{"q": "累積相對次數折線圖有什麼用？",
            "a": "一眼就能看出「未滿某個值」的人占多少百分比，例如成績未滿 60 分的有百分之幾；最後一點一定是 100%。"},
           {"q": "累積次數和累積相對次數差在哪？",
            "a": "累積次數是人數（或次數），累積相對次數是除以總數後的百分比，方便比較人數不同的兩班。"},
           {"q": "八年級的統計要學什麼？",
            "a": "108課綱 D-8-1：統計資料處理，包含累積次數、相對次數、累積相對次數折線圖。"}]
    make_unit(R, "grade-8", "cumulative-relative-frequency", "D-8-1",
              "統計資料處理：累積次數、相對次數、累積相對次數折線圖。",
              "累積次數與累積相對次數折線圖",
              "八年級數學 累積相對次數 練習題｜累積次數・相對次數・折線圖 學習單（附解答）",
              "累積相對次數",
              "國中八年級數學「累積次數與累積相對次數折線圖」免費學習單：從次數分配表求累積次數、相對次數、累積相對次數，「以上」的百分比，讀累積相對次數折線圖和應用題。100題線上練習馬上對答案，附可列印解答。",
              "累積相對次數 ＝ 累積次數 ÷ 總次數",
              "「以上」用 100% 去減；兩點相減就是一組的相對次數。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
