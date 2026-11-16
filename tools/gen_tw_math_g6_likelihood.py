# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：可能性（108課綱 D-6-2）
  python3 tools/gen_tw_math_g6_likelihood.py
「一定會」「很有可能」「很不可能」「不可能」、Ａ比Ｂ可能（箱の中の球の數）、統計圖表から可能性を判斷、轉盤・骰子・抽卡、說明。
誤答：少ないものが出やすいと思う、前の結果に引きずられる（連続で表だから次は裏）、「可能」と「一定」を混同。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, fig, svg_wrap, text
import math

R = random.Random(61019)
NM = Names(R)
COLS = {"紅": "#c0392b", "藍": "#1f5fa8", "黃": "#e0a030", "綠": "#2e7d4f", "白": "#ffffff"}


def box_svg(counts):
    """袋子の中の球"""
    balls = [c for c, n in counts for _ in range(n)]
    R.shuffle(balls)
    W = 30 + min(len(balls), 10) * 26
    rows = (len(balls) + 9) // 10
    H = 30 + rows * 26
    s = ["<rect x='4' y='4' width='%d' height='%d' rx='10' fill='#f6f3ec' stroke='#8a8378' stroke-width='2'/>" % (W - 8, H - 8)]
    for i, c in enumerate(balls):
        x, y = 26 + (i % 10) * 26, 26 + (i // 10) * 26
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s' stroke='#2b2b2b' stroke-width='1.2'/>" % (x, y, COLS[c]))
        s.append(text(x, y + 4, c, 9, col="#fff" if c not in ("黃", "白") else "#2b2b2b"))
    return fig(svg_wrap(W, H, "".join(s), "袋子裡的球：" + "、".join("%s球 %d 顆" % (c, n) for c, n in counts)))


def spinner(parts):
    """parts: [(color, 等分數)]"""
    tot = sum(n for _, n in parts)
    W = H = 170
    cx = cy = 85
    r = 72
    s = []
    a0 = -90.0
    for c, n in parts:
        for _ in range(n):
            a1 = a0 + 360 / tot
            x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
            x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='#2b2b2b' stroke-width='1.2'/>" % (cx, cy, x0, y0, r, r, x1, y1, COLS[c]))
            mid = math.radians((a0 + a1) / 2)
            s.append(text(cx + r * .62 * math.cos(mid), cy + r * .62 * math.sin(mid) + 4, c, 11, col="#fff" if c not in ("黃", "白") else "#2b2b2b"))
            a0 = a1
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#2b2b2b' stroke-width='3'/>" % (cx, cy, cx, cy - 50))
    s.append("<circle cx='%d' cy='%d' r='5' fill='#2b2b2b'/>" % (cx, cy))
    return fig(svg_wrap(W, H, "".join(s), "轉盤：" + "、".join("%s色 %d 格" % (c, n) for c, n in parts)))


def s1(seen):
    EV = [("明天太陽會從東邊升起。", "一定會"), ("丟一顆骰子，出現 7 點。", "不可能"), ("丟一枚硬幣，出現正面。", "可能會，也可能不會"),
          ("袋子裡只有紅球，摸出一顆是紅球。", "一定會"), ("袋子裡只有紅球，摸出一顆是藍球。", "不可能"), ("丟一顆骰子，出現的點數小於 7。", "一定會"),
          ("丟一顆骰子，出現 3 點。", "可能會，也可能不會"), ("一年有 13 個月。", "不可能"), ("明天會下雨。", "可能會，也可能不會"),
          ("從 1 到 10 的數字卡抽一張，是偶數。", "可能會，也可能不會"), ("從 1 到 10 的數字卡抽一張，數字比 0 大。", "一定會"), ("水在 0 度以下會結冰。", "一定會")]
    out = []
    for st, ans in EV:
        out.append(mcq("「%s」這件事是？" % st, ans, [x for x in ("一定會", "不可能", "可能會，也可能不會", "一定不會發生，因為沒看過") if x != ans][:3],
                       {"一定會": "每一次都會發生。", "不可能": "絕對不會發生。", "可能會，也可能不會": "有時會發生，有時不會。"}[ans]))
    for o in out:
        seen.add(o["q"])

    def big():
        a, b = R.randint(1, 3), R.randint(12, 19)
        c1, c2 = R.sample(["紅", "藍", "黃", "綠"], 2)
        q = "袋子裡有%s球 %d 顆、%s球 %d 顆。摸出一顆是%s球，可能性是？" % (c1, a, c2, b, c1)
        return mcq(q, "很不可能", ["很有可能", "一定會", "不可能"], "%s球只有 %d 顆，比 %s球少很多，很不可能摸到，但不是不可能。" % (c1, a, c2))
    return out + pick_unique(R, big, 8, seen)


def s2(seen):
    def mk():
        cs = R.sample(["紅", "藍", "黃", "綠"], 3)
        ns = R.sample(range(1, 9), len(cs))
        counts = list(zip(cs, ns))
        g = box_svg(counts)
        mx = max(ns)
        ans = cs[ns.index(mx)]
        kind = R.choice(["max", "min"])
        if kind == "min":
            mn = min(ns)
            ans = cs[ns.index(mn)]
            q = "從袋子裡摸出一顆球，最不可能摸到哪一種顏色？" + g
            e = "%s球最少（%d 顆），最不可能摸到。" % (ans, mn)
        else:
            q = "從袋子裡摸出一顆球，最有可能摸到哪一種顏色？" + g
            e = "%s球最多（%d 顆），最有可能摸到。" % (ans, mx)
        w = [c + "球" for c in cs if c != ans] + ["每種都一樣"]
        return mcq(q, ans + "球", w, e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        cs = R.sample(["紅", "藍", "黃", "綠"], R.choice([2, 3]))
        ns = R.sample(range(1, 6), len(cs))
        parts = list(zip(cs, ns))
        g = spinner(parts)
        i, j = R.sample(range(len(cs)), 2)
        q = "轉動轉盤，指針停在%s色和%s色，哪一個比較可能？" % (cs[i], cs[j]) + g
        if ns[i] == ns[j]:
            return None
        ans = cs[i] + "色" if ns[i] > ns[j] else cs[j] + "色"
        oth = cs[j] + "色" if ans == cs[i] + "色" else cs[i] + "色"
        return mcq(q, ans, [oth, "一樣可能", "看轉的力氣，無法比較"], "%s占的格子比較多（%d 格比 %d 格），比較可能。" % (ans, max(ns[i], ns[j]), min(ns[i], ns[j])))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        names = ["小明", "小華", "小美", "家豪"]
        k = R.randint(3, 4)
        ns = R.sample(range(2, 10), k)
        who = names[:k]
        tb = table(["投籃的人"] + who, [["10 次中投進的次數"] + [str(min(n, 10)) for n in ns]])
        ns = [min(n, 10) for n in ns]
        if len(set(ns)) < k:
            return None
        mx = max(ns)
        ans = who[ns.index(mx)]
        q = "下表是同學練習投籃的紀錄。下一次投籃，誰最有可能投進？" + tb
        return mcq(q, ans, [w for w in who if w != ans][:2] + ["每個人都一樣"], "%s 10 次投進 %d 次最多，從紀錄看最有可能投進。" % (ans, mx))

    def weather():
        rain = R.randint(1, 29)
        sun = 30 - rain
        q = "某地過去 30 天中，下雨 %d 天、沒下雨 %d 天。明天下雨的可能性怎麼說比較合理？" % (rain, sun)
        if rain >= 24:
            ans = "很有可能下雨"
        elif rain <= 6:
            ans = "很不可能下雨"
        else:
            return None
        w = ["一定會下雨" if ans == "很有可能下雨" else "不可能下雨", "很不可能下雨" if ans == "很有可能下雨" else "很有可能下雨", "一定不會下雨" if ans == "很有可能下雨" else "一定會下雨"]
        return mcq(q, ans, w, "從資料看，下雨的天數%s，但天氣不能百分之百確定，所以說「%s」。" % ("很多" if rain >= 24 else "很少", ans))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, weather, 8, seen)


def s5(seen):
    def coin():
        k = R.randint(3, 6)
        q = "丟一枚硬幣，已經連續出現 %d 次正面。下一次出現反面的可能性和出現正面比，怎樣？" % k
        return mcq(q, "一樣可能", ["反面比較可能", "正面比較可能", "一定是反面"], "每一次丟硬幣都和前面無關，正面和反面一樣可能。")

    def dice():
        F_ = [("丟一顆骰子，出現偶數和出現奇數，哪一個比較可能？", "一樣可能", ["偶數", "奇數", "無法判斷"], "偶數 2、4、6，奇數 1、3、5，都是 3 種。"),
              ("丟一顆骰子，出現大於 4 的點數和小於 5 的點數，哪一個比較可能？", "小於 5", ["大於 4", "一樣可能", "無法判斷"], "大於 4：5、6（2 種）；小於 5：1、2、3、4（4 種）。"),
              ("丟一顆骰子，出現 6 點和出現 1 點，哪一個比較可能？", "一樣可能", ["6 點", "1 點", "看運氣"], "每一面都一樣可能出現。"),
              ("丟一顆骰子，出現 3 的倍數和出現 1 點，哪一個比較可能？", "3 的倍數", ["1 點", "一樣可能", "無法判斷"], "3 的倍數有 3 和 6 兩種，比 1 點多。")]
        return mcq(*R.choice(F_))

    def cards():
        n = R.randint(10, 30)
        a = R.choice([2, 3, 5])
        cnt = n // a
        other = n - cnt
        q = "從 1 到 %d 的數字卡抽一張。抽到「%d 的倍數」和「不是 %d 的倍數」，哪一個比較可能？" % (n, a, a)
        ans = "不是 %d 的倍數" % a if other > cnt else ("%d 的倍數" % a if cnt > other else "一樣可能")
        w = [x for x in ("%d 的倍數" % a, "不是 %d 的倍數" % a, "一樣可能", "無法判斷") if x != ans][:3]
        return mcq(q, ans, w, "%d 的倍數有 %d 張，不是的有 %d 張。" % (a, cnt, other))
    return pick_unique(R, coin, 4, seen) + pick_unique(R, dice, 4, seen) + pick_unique(R, cards, 12, seen)


def main():
    seen = set()
    sets = [("一定、可能、不可能", s1(seen)), ("摸球的可能性", s2(seen)), ("轉盤：哪一個比較可能", s3(seen)),
            ("從統計資料判斷", s4(seen)), ("骰子、硬幣和數字卡", s5(seen))]
    body = lesson(
        ["事情發生的可能性：<b>一定會</b>、<b>很有可能</b>、<b>可能會也可能不會</b>、<b>很不可能</b>、<b>不可能</b>。",
         "比較可能性：哪一種的數量（球的顆數、轉盤的格數）越多，就越可能出現。",
         "看統計資料可以判斷誰比較可能；但每一次丟硬幣、骰子都和前一次無關。"],
        [example("袋子裡紅球 8 顆、藍球 2 顆，摸到哪一種比較可能？", ["紅球比較多。"], "紅球"),
         example("硬幣連續 5 次正面，下一次呢？", ["每次都和前面無關。"], "正面和反面一樣可能")],
        [("藍球只有 1 顆，就說不可能摸到", "只是很不可能，還是有機會"),
         ("連續正面，下次一定是反面", "每次都一樣可能"),
         ("數量少的比較容易出現", "數量多的比較可能")])
    faq = [{"q": "「很不可能」和「不可能」有什麼不同？",
            "a": "不可能是一定不會發生（例如骰子丟出 7 點）；很不可能是機會很小，但還是可能發生（例如 20 顆球裡只有 1 顆紅球）。"},
           {"q": "連續丟出 5 次正面，下一次會比較容易出現反面嗎？",
            "a": "不會。每一次丟硬幣都是獨立的，正面和反面的可能性一樣。"},
           {"q": "六年級的可能性要學什麼？",
            "a": "108課綱 D-6-2：從統計圖表資料回答可能性問題，是機率的前置經驗，包含「很有可能」、「很不可能」、「Ａ比Ｂ可能」。"}]
    make_unit(R, "grade-6", "likelihood", "D-6-2",
              "解題：可能性。從統計圖表資料，回答可能性問題。機率前置經驗。「很有可能」、「很不可能」、「Ａ比Ｂ可能」。",
              "可能性",
              "六年級數學 可能性 練習題｜一定・很有可能・不可能・摸球轉盤 學習單（附解答）",
              "可能性",
              "國小六年級數學「可能性」免費學習單：一定會、很有可能、很不可能、不可能，摸球和轉盤比較可能性、從統計資料判斷，以及骰子、硬幣和數字卡。100題線上練習馬上對答案，附可列印解答。",
              "數量越多，越可能出現",
              "每一次丟硬幣都和前一次無關。",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
