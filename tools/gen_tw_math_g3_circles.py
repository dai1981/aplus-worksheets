# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：圓（108課綱 S-3-3）
  python3 tools/gen_tw_math_g3_circles.py
圓心・圓周・半徑・直徑の名前、直徑＝半徑×2、圓規で指定の半径の円を描く、圓の並び、性質。
誤答：直徑と半徑の取り違え、圓規を直徑の長さに開く、圓心を通らない線を直徑とする。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK, RED, BLUE

R = random.Random(31019)
NM = Names(R)
LET = "甲乙丙丁"


def parts_svg(order):
    """order：[圓心, 半徑, 直徑, 不通過圓心的線] を 甲乙丙丁 に割り当てる"""
    cx, cy, r = 130, 110, 90
    s = ["<circle cx='%d' cy='%d' r='%d' fill='#fff' stroke='%s' stroke-width='3'/>" % (cx, cy, r, GREEN)]
    rot = R.choice([0, 20, -25, 40])
    a = math.radians(rot)
    for kind, lab in zip(order, LET):
        if kind == "center":
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (cx, cy, INK))
            s.append(text(cx - 14, cy - 8, lab, 16))
        elif kind == "radius":
            b = a + math.radians(110)
            x, y = cx + r * math.cos(b), cy + r * math.sin(b)
            s.append(line(cx, cy, x, y, BLUE, 3))
            s.append(text((cx + x) / 2 - 14, (cy + y) / 2, lab, 16, col=BLUE))
        elif kind == "diam":
            x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
            x2, y2 = cx - r * math.cos(a), cy - r * math.sin(a)
            s.append(line(x1, y1, x2, y2, RED, 3))
            s.append(text(x1 + 12 * math.cos(a) + 6, y1 + 12 * math.sin(a) + 5, lab, 16, col=RED))
        else:
            b1, b2 = a + math.radians(200), a + math.radians(290)
            x1, y1 = cx + r * math.cos(b1), cy + r * math.sin(b1)
            x2, y2 = cx + r * math.cos(b2), cy + r * math.sin(b2)
            s.append(line(x1, y1, x2, y2, INK, 3, " stroke-dasharray='6 4'"))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            s.append(text(mx + (mx - cx) * .25, my + (my - cy) * .25 + 5, lab, 16))
    return fig(svg_wrap(260, 220, "".join(s), "圓上標了甲乙丙丁"))


def s1(seen):
    NAME = {"center": "圓心", "radius": "半徑", "diam": "直徑"}

    def mk():
        order = ["center", "radius", "diam", "chord"]
        R.shuffle(order)
        ask = R.choice(["center", "radius", "diam", "diam"])
        ans = LET[order.index(ask)]
        q = "圖中哪一個是<b>%s</b>？" % NAME[ask] + parts_svg(order)
        e = {"center": "圓中心的點是圓心。", "radius": "從圓心連到圓周的線是半徑。",
             "diam": "通過圓心、兩端都在圓周上的線是直徑。"}[ask]
        if ask == "diam":
            e += "%s沒有通過圓心，不是直徑。" % LET[order.index("chord")]
        return mcq(q, ans, [l for l in LET if l != ans], e)
    words = [mcq("圓中心的那一點叫做什麼？", "圓心", ["圓周", "半徑", "直徑"], "圓中心的點叫做圓心。"),
             mcq("圓外圍一圈的線叫做什麼？", "圓周", ["圓心", "半徑", "直徑"], "圓外圍一圈的線叫做圓周。"),
             mcq("從圓心連到圓周上一點的線叫做什麼？", "半徑", ["直徑", "圓周", "圓心"], "從圓心到圓周的線是半徑。"),
             mcq("通過圓心、兩端都在圓周上的線叫做什麼？", "直徑", ["半徑", "圓周", "圓心"], "通過圓心、兩端在圓周上的線是直徑。")]
    for w in words:
        seen.add(w["q"])
    return words + pick_unique(R, mk, 16, seen)


def s2(seen):
    def r2d():
        r = R.randint(2, 30)
        q = "一個圓的半徑是 %d 公分，直徑是幾公分？" % r
        return mcq(q, "%d 公分" % (2 * r), ["%d 公分" % x for x in (r, r // 2 if r % 2 == 0 else r + 2, 4 * r, r + 2)], "直徑 ＝ 半徑 × 2：%d × 2 ＝ %d（公分）。" % (r, 2 * r))

    def d2r():
        r = R.randint(2, 30)
        q = "一個圓的直徑是 %d 公分，半徑是幾公分？" % (2 * r)
        return mcq(q, "%d 公分" % r, ["%d 公分" % x for x in (2 * r, 4 * r, r + 2, r - 1)], "半徑 ＝ 直徑 ÷ 2：%d ÷ 2 ＝ %d（公分）。" % (2 * r, r))
    return pick_unique(R, r2d, 10, seen) + pick_unique(R, d2r, 10, seen)


def s3(seen):
    def open_r():
        r = R.randint(2, 12)
        q = "圓規的兩腳張開 %d 公分，畫出的圓<b>直徑</b>是幾公分？" % r
        return mcq(q, "%d 公分" % (2 * r), ["%d 公分" % x for x in (r, r + 2, 4 * r)], "圓規張開的長度是半徑 %d 公分，直徑是 %d × 2 ＝ %d 公分。" % (r, r, 2 * r))

    def need():
        r = R.randint(2, 12)
        q = "要用圓規畫一個直徑 %d 公分的圓，圓規的兩腳要張開幾公分？" % (2 * r)
        return mcq(q, "%d 公分" % r, ["%d 公分" % x for x in (2 * r, 4 * r, r + 1)], "圓規張開的長度是半徑：%d ÷ 2 ＝ %d 公分。" % (2 * r, r))

    STEPS = [("用圓規畫圓時，圓規的針腳要放在哪裡？", "圓心", ["圓周上", "直徑的一端", "紙的角落"], "針腳固定在圓心，筆腳轉一圈畫出圓周。"),
             ("用圓規畫圓時，兩腳張開的長度是圓的什麼？", "半徑", ["直徑", "圓周", "圓心"], "圓規兩腳的距離就是半徑。"),
             ("畫圓時，為什麼圓周上每一點到圓心都一樣遠？", "因為圓規張開的長度不變", ["因為筆比較尖", "因為紙是白色的", "因為轉得很快"], "圓規兩腳的距離不變，所以每一點到圓心的距離都等於半徑。"),
             ("畫好一個圓後，圓規張開得更大再畫一個圓，新的圓會怎樣？", "比較大", ["比較小", "一樣大", "變成正方形"], "張開得越大，半徑越長，圓就越大。")]
    out = [mcq(*x) for x in STEPS]
    for w in out:
        seen.add(w["q"])
    return out + pick_unique(R, open_r, 8, seen) + pick_unique(R, need, 8, seen)


def row_svg(n, r_px=30):
    s = ["<rect x='10' y='10' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (2 * r_px * n, 2 * r_px, INK)]
    for i in range(n):
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (10 + r_px + 2 * r_px * i, 10 + r_px, r_px, FILL, GREEN))
    return fig(svg_wrap(2 * r_px * n + 20, 2 * r_px + 20, "".join(s), "%d 個一樣大的圓排在長方形裡" % n))


def s4(seen):
    def row():
        n = R.randint(2, 5)
        r = R.randint(2, 9)
        if R.random() < .5:
            q = "%d 個一樣大的圓剛好排在長方形裡，每個圓的半徑是 %d 公分。長方形的長是幾公分？" % (n, r) + row_svg(n)
            a = 2 * r * n
            return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (r * n, 2 * r, 2 * r * n + 2 * r, 4 * r * n)],
                       "1 個圓的直徑是 %d × 2 ＝ %d 公分，%d 個是 %d × %d ＝ %d 公分。" % (r, 2 * r, n, 2 * r, n, a))
        q = "%d 個一樣大的圓剛好排在長方形裡，長方形的長是 %d 公分。每個圓的半徑是幾公分？" % (n, 2 * r * n) + row_svg(n)
        return mcq(q, "%d 公分" % r, ["%d 公分" % x for x in (2 * r, r * n, 2 * r * n // n + 1, r + n)],
                   "1 個圓的直徑是 %d ÷ %d ＝ %d 公分，半徑是 %d ÷ 2 ＝ %d 公分。" % (2 * r * n, n, 2 * r, 2 * r, r))

    def square():
        a = R.randint(3, 20) * 2
        q = "在邊長 %d 公分的正方形裡畫一個最大的圓，圓的半徑是幾公分？" % a
        return mcq(q, "%d 公分" % (a // 2), ["%d 公分" % x for x in (a, a * 2, a // 2 + 2, a * 4)], "最大的圓直徑等於正方形的邊長 %d 公分，半徑是 %d 公分。" % (a, a // 2))
    return pick_unique(R, row, 12, seen) + pick_unique(R, square, 8, seen)


TRUE = ["同一個圓的半徑都一樣長。", "同一個圓的直徑是半徑的 2 倍。", "直徑一定通過圓心。", "一個圓有無數條半徑。",
        "圓周上每一點到圓心的距離都一樣。", "圓規張開的長度就是半徑。"]
FALSE = ["同一個圓的半徑有長有短。", "直徑是半徑的一半。", "圓周上兩點連成的線都是直徑。", "一個圓只有 2 條半徑。",
         "圓規張開的長度是直徑。", "半徑一定是橫的線。"]


def s5(seen):
    def stmt():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s 圓心到圓周的線是半徑，同一個圓的半徑都一樣長；直徑通過圓心，是半徑的 2 倍。" % (LET[k], ans))

    def life():
        who = NM.next()
        kind = R.choice(["wheel", "hoop", "plate"])
        if kind == "wheel":
            d = R.randint(20, 70) * 2
            q = "一個腳踏車輪子的直徑是 %d 公分，從輪子中心到輪胎外圈是幾公分？" % d
            return mcq(q, "%d 公分" % (d // 2), ["%d 公分" % x for x in (d, d * 2, d // 2 + 10)], "中心到外圈是半徑：%d ÷ 2 ＝ %d（公分）。" % (d, d // 2))
        if kind == "hoop":
            r = R.randint(30, 50)
            q = "%s的呼拉圈半徑是 %d 公分，呼拉圈的直徑是幾公分？" % (who, r)
            return mcq(q, "%d 公分" % (2 * r), ["%d 公分" % x for x in (r, r // 2 if r % 2 == 0 else r + 5, 4 * r)], "直徑 ＝ 半徑 × 2：%d × 2 ＝ %d（公分）。" % (r, 2 * r))
        r = R.randint(8, 15)
        n = R.randint(2, 4)
        q = "%d 個半徑 %d 公分的盤子在桌上排成一排，邊緣互相碰到，這一排一共長幾公分？" % (n, r)
        return mcq(q, "%d 公分" % (2 * r * n), ["%d 公分" % x for x in (r * n, 2 * r, 2 * r * n + r)], "每個盤子的直徑 %d 公分，%d × %d ＝ %d（公分）。" % (2 * r, 2 * r, n, 2 * r * n))
    return pick_unique(R, stmt, 10, seen) + pick_unique(R, life, 10, seen)


def main():
    seen = set()
    sets = [("圓心、圓周、半徑、直徑", s1(seen)), ("半徑和直徑", s2(seen)), ("用圓規畫圓", s3(seen)),
            ("圓排一排", s4(seen)), ("圓的性質和生活中的圓", s5(seen))]
    demo = parts_svg(["center", "radius", "diam", "chord"])
    body = lesson(
        ["圓的中心叫<b>圓心</b>，外圍一圈的線叫<b>圓周</b>。",
         "從圓心到圓周的線是<b>半徑</b>；通過圓心、兩端在圓周上的線是<b>直徑</b>。",
         "同一個圓：半徑都一樣長，<b>直徑 ＝ 半徑 × 2</b>。",
         "用圓規畫圓：針腳放在圓心，兩腳張開的長度就是<b>半徑</b>。"],
        [example("找一找：甲是圓心，乙是半徑，丙是直徑，丁沒有通過圓心。" + demo, ["丁的兩端在圓周上，但沒有通過圓心，所以不是直徑。"], "丙是直徑"),
         example("要畫直徑 8 公分的圓，圓規要張開幾公分？", ["圓規張開的長度是半徑。", "8 ÷ 2 ＝ 4。"], "4 公分")],
        [("直徑是半徑的一半", "直徑是半徑的 2 倍"),
         ("圓規張開的長度是直徑", "圓規張開的長度是半徑"),
         ("圓周上兩點連起來就是直徑", "一定要通過圓心才是直徑")])
    faq = [{"q": "三年級的圓要學什麼？",
            "a": "108課綱 S-3-3：認識圓心、圓周、半徑和直徑，知道直徑是半徑的 2 倍，會用圓規畫指定半徑的圓。圓周長和圓面積在五、六年級學。"},
           {"q": "怎麼教孩子使用圓規？",
            "a": "先用尺量好半徑，把圓規張開到這個長度；針腳壓在圓心不動，拿著圓規頭輕輕轉一圈。"},
           {"q": "半徑和直徑怎麼記？",
            "a": "半徑是「一半」的長度：從圓心走到圓周；直徑是「直直穿過」圓心，從圓周走到另一邊，所以是半徑的 2 倍。"}]
    make_unit(R, "grade-3", "circles", "S-3-3",
              "圓：「圓心」、「圓周」、「半徑」與「直徑」。能使用圓規畫指定半徑的圓。",
              "圓：圓心、圓周、半徑、直徑",
              "三年級數學 圓 練習題｜圓心・半徑・直徑・圓規 學習單（附解答）",
              "圓",
              "國小三年級數學「圓」免費學習單：認識圓心、圓周、半徑、直徑，直徑是半徑的2倍，用圓規畫圓，圓排一排和生活中的圓。100題線上練習馬上對答案，附可列印解答。",
              "直徑 ＝ 半徑 × 2",
              "圓規張開的長度是半徑；直徑一定通過圓心。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
