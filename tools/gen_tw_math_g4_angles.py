# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：角度（度、量角器、平角、周角）（108課綱 N-4-10／S-4-1）
  python3 tools/gen_tw_math_g4_angles.py
量角器の読み取り、銳角・直角・鈍角・平角・周角、角的合成（平角・周角から求める）、180〜360 度の角、三角板の組み合わせ。
誤答：量角器の外側と内側の目盛りを取り違える（x と 180−x）、平角を 90 度とする、360 から引き忘れる。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, INK, RED, BLUE

R = random.Random(41011)
NM = Names(R)


def protractor(deg, flip=False):
    """量角器（外側：右 0→左 180、内側：左 0→右 180）。始邊は flip=False なら右、True なら左"""
    cx, cy, r = 200, 190, 170
    s = ["<path d='M%d %d A%d %d 0 0 0 %d %d Z' fill='#f4f8f5' stroke='%s' stroke-width='2'/>" % (cx + r, cy, r, r, cx - r, cy, GREEN)]
    for i in range(0, 181):
        a = math.radians(180 - i)
        L = 14 if i % 10 == 0 else (9 if i % 5 == 0 else 5)
        x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
        x2, y2 = cx + (r - L) * math.cos(a), cy - (r - L) * math.sin(a)
        s.append(line(x1, y1, x2, y2, INK, 1.2 if i % 10 == 0 else .7))
        if i % 10 == 0:
            ro, ri = r - 26, r - 46
            dy = -10 if i in (0, 180) else 0
            # 外側：右 0（i=180 の位置が右端）
            s.append(text(cx + ro * math.cos(a), cy - ro * math.sin(a) + 4 + dy, str(180 - i), 11))
            s.append(text(cx + ri * math.cos(a), cy - ri * math.sin(a) + 4 + dy, str(i), 9, col=BLUE, weight=400))
    base = 0 if not flip else 180
    a1 = math.radians(base)
    a2 = math.radians(base + (deg if not flip else -deg))
    for a, col in ((a1, RED), (a2, RED)):
        s.append(line(cx, cy, cx + (r + 22) * math.cos(a), cy - (r + 22) * math.sin(a), col, 3))
    s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, RED))
    return fig(svg_wrap(400, 205, "".join(s), "量角器量角"))


def s1(seen):
    def mk():
        deg = R.choice([x for x in range(10, 171, 5) if x != 90])
        flip = R.random() < .4
        q = "看量角器，紅色的角是幾度？" + protractor(deg, flip)
        return mcq(q, "%d 度" % deg, ["%d 度" % x for x in (180 - deg, deg + 10, deg - 10, deg + 5)],
                   "%s的邊對準 0 度，要讀%s那一圈的刻度：%d 度。%s" % ("右邊" if not flip else "左邊", "外" if not flip else "內", deg,
                                                       "（%d 度是讀錯了另一圈）" % (180 - deg)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        kind = R.choice(["銳角", "直角", "鈍角", "平角", "周角", "銳角", "鈍角"])
        deg = {"銳角": R.randint(5, 85), "直角": 90, "鈍角": R.randint(95, 175), "平角": 180, "周角": 360}[kind]
        q = "%d 度的角是什麼角？" % deg
        return mcq(q, kind, [k for k in ("銳角", "直角", "鈍角", "平角", "周角") if k != kind][:3] if kind not in ("周角",) else ["平角", "鈍角", "直角"],
                   "比 90 度小是銳角，90 度是直角，比 90 度大、比 180 度小是鈍角，180 度是平角，360 度是周角。")

    def facts():
        F = [("1 個平角是幾度？", "180 度", ["90 度", "360 度", "100 度"], "平角是一直線，180 度。"),
             ("1 個周角是幾度？", "360 度", ["180 度", "100 度", "400 度"], "轉一整圈是周角，360 度。"),
             ("1 個平角等於幾個直角？", "2 個", ["1 個", "3 個", "4 個"], "180 ÷ 90 ＝ 2。"),
             ("1 個周角等於幾個直角？", "4 個", ["2 個", "3 個", "6 個"], "360 ÷ 90 ＝ 4。"),
             ("1 個周角等於幾個平角？", "2 個", ["1 個", "3 個", "4 個"], "360 ÷ 180 ＝ 2。"),
             ("量角器上的 1 小格是幾度？", "1 度", ["10 度", "5 度", "0.1 度"], "量角器把半圓分成 180 小格，1 小格是 1 度。")]
        f = R.choice(F)
        return mcq(*f)
    return pick_unique(R, mk, 14, seen) + pick_unique(R, facts, 6, seen)


def s3(seen):
    def line_q():
        a = R.randint(15, 165)
        q = "兩個角合起來是一個平角，其中一個角是 %d 度，另一個角是幾度？" % a
        return mcq(q, "%d 度" % (180 - a), ["%d 度" % x for x in (90 - a if a < 90 else a - 90, 360 - a, 180 + a if 180 + a < 360 else a, 170 - a if a < 170 else 185 - a)],
                   "平角是 180 度：180 － %d ＝ %d（度）。" % (a, 180 - a))

    def point():
        a, b = R.randint(40, 150), R.randint(40, 150)
        c = 360 - a - b
        if c < 20:
            return None
        q = "三個角圍成一個周角，其中兩個是 %d 度和 %d 度，第三個角是幾度？" % (a, b)
        return mcq(q, "%d 度" % c, ["%d 度" % x for x in (180 - a - b if a + b < 180 else c + 180, c + 10, c - 10, a + b)],
                   "周角是 360 度：360 － %d － %d ＝ %d（度）。" % (a, b, c))

    def join():
        a, b = R.randint(15, 120), R.randint(15, 120)
        q = "%d 度的角和 %d 度的角拼在一起（頂點和一條邊對齊），合成的角是幾度？" % (a, b)
        return mcq(q, "%d 度" % (a + b), ["%d 度" % x for x in (abs(a - b) if a != b else a + b + 10, a + b + 10, 180 - a - b if a + b < 180 else a + b - 10)],
                   "角的合成用加法：%d ＋ %d ＝ %d（度）。" % (a, b, a + b))
    return pick_unique(R, line_q, 8, seen) + pick_unique(R, point, 6, seen) + pick_unique(R, join, 6, seen)


def s4(seen):
    def mk():
        a = R.choice(range(20, 171, 5))
        if R.random() < .5:
            q = "一個角是 %d 度，它外面的角（合起來是周角）是幾度？" % a
            return mcq(q, "%d 度" % (360 - a), ["%d 度" % x for x in (180 - a, 360 + a if 360 + a < 500 else 350 - a, 270 - a if a < 270 else 300 - a)],
                       "周角是 360 度：360 － %d ＝ %d（度）。" % (a, 360 - a))
        b = R.choice(range(5, 180, 5))
        v = 180 + b
        q = "一個角是 1 個平角再多 %d 度，這個角是幾度？" % b
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (180 - b, 90 + b, 360 - b, v + 10, v - 10)], "180 ＋ %d ＝ %d（度），比平角大、比周角小。" % (b, v))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    TRI = [30, 45, 60, 90]

    def mk():
        a, b = R.sample(TRI, 2)
        if R.random() < .6:
            q = "用兩個三角板的 %d 度角和 %d 度角拼在一起，可以拼出幾度的角？" % (a, b)
            return mcq(q, "%d 度" % (a + b), ["%d 度" % x for x in (abs(a - b), a + b + 15, a * b // 10 if a * b // 10 != a + b else a + b - 15, 180 - a - b if 180 - a - b > 0 else a + b + 30)],
                       "%d ＋ %d ＝ %d（度）。" % (a, b, a + b))
        big, small = max(a, b), min(a, b)
        q = "用三角板的 %d 度角減去 %d 度角，可以畫出幾度的角？" % (big, small)
        return mcq(q, "%d 度" % (big - small), ["%d 度" % x for x in (big + small, big - small + 15, 180 - big + small, big - small + 30)],
                   "%d － %d ＝ %d（度）。" % (big, small, big - small))

    def est():
        deg = R.choice([25, 40, 75, 110, 135, 160])
        q = "這個角大約是幾度？" + fig(svg_wrap(240, 140, line(30, 120, 220, 120, INK, 3) + line(30, 120, 30 + 150 * math.cos(math.radians(deg)), 120 - 150 * math.sin(math.radians(deg)), INK, 3) if deg <= 90 else
                                            line(130, 120, 230, 120, INK, 3) + line(130, 120, 130 + 110 * math.cos(math.radians(deg)), 120 - 110 * math.sin(math.radians(deg)), INK, 3), "一個角"))
        opts = {25: ["25 度", "60 度", "100 度", "150 度"], 40: ["40 度", "10 度", "80 度", "140 度"], 75: ["75 度", "30 度", "120 度", "160 度"],
                110: ["110 度", "60 度", "160 度", "30 度"], 135: ["135 度", "90 度", "45 度", "170 度"], 160: ["160 度", "110 度", "60 度", "20 度"]}[deg]
        return mcq(q, opts[0], opts[1:], "和直角（90 度）、平角（180 度）比一比：大約 %d 度。" % deg)
    return pick_unique(R, mk, 14, seen) + pick_unique(R, est, 6, seen)


def main():
    seen = set()
    sets = [("用量角器量角", s1(seen)), ("銳角、直角、鈍角、平角、周角", s2(seen)), ("角的合成", s3(seen)),
            ("比平角大的角", s4(seen)), ("三角板和估測", s5(seen))]
    body = lesson(
        ["角的大小用<b>度</b>表示，1 度寫成 1°。量角器的中心對準角的頂點，0 度線對準一條邊。",
         "<b>要讀和 0 度同一圈的刻度</b>：邊對準右邊的 0，讀外圈；對準左邊的 0，讀內圈。",
         "比 90 度小是<b>銳角</b>，90 度是<b>直角</b>，90〜180 度是<b>鈍角</b>，180 度是<b>平角</b>，360 度是<b>周角</b>。",
         "角可以合成：一直線上的角加起來是 180 度，繞一圈的角加起來是 360 度。"],
        [example("一個平角分成兩個角，一個是 65 度，另一個是幾度？", ["平角是 180 度。", "180 － 65 ＝ 115。"], "115 度"),
         example("三角板的 45 度角和 60 度角拼起來是幾度？", ["45 ＋ 60 ＝ 105。"], "105 度")],
        [("讀錯量角器的那一圈（讀成 180 減去答案）", "先找邊對準的 0 度在哪一圈，就讀那一圈"),
         ("平角是 90 度", "平角是一直線，180 度"),
         ("周角裡的另一個角直接用 180 去減", "繞一圈是 360 度，要用 360 去減")])
    faq = [{"q": "量角器怎麼讀才不會錯？",
            "a": "量角器有內外兩圈刻度。角的一條邊對準哪一邊的 0 度，就讀那一圈；讀完再看角是銳角還是鈍角，檢查答案合不合理。"},
           {"q": "四年級的角度要學什麼？",
            "a": "108課綱 N-4-10／S-4-1：認識「度」，用量角器量角和畫角，估測和計算角度，用角的合成認識 180 到 360 度的角、平角和周角。"},
           {"q": "銳角和鈍角怎麼分？",
            "a": "比直角（90 度）小的是銳角，比直角大、比平角（180 度）小的是鈍角。"}]
    make_unit(R, "grade-4", "angles", "N-4-10",
              "角度：「度」（同 S-4-1）。量角器的操作。實測、估測與計算。以角的合成認識 180 度到 360 度之間的角度。「平角」、「周角」。指定角度作圖。",
              "角度：量角器、平角與周角",
              "四年級數學 角度 練習題｜量角器・銳角鈍角・平角周角 學習單（附解答）",
              "角度與量角器",
              "國小四年級數學「角度」免費學習單：用量角器量角、銳角直角鈍角平角周角、角的合成、比平角大的角和三角板拼角。100題線上練習馬上對答案，附可列印解答。",
              "讀和 0 度同一圈的刻度",
              "平角 180 度，周角 360 度。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
