# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：地圖比例尺（108課綱 S-6-2）
  python3 tools/gen_tw_math_g6_map_scales.py
比例尺の意味（1：10000＝圖上 1 公分是實際 10000 公分＝100 公尺）、圖上距離→實際距離、實際距離→圖上距離、比例尺を求める、線段比例尺・應用。
誤答：公分→公尺・公里の換算を忘れる、掛けるべきところで割る、比例尺の前後を逆にする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num, dnum, fig, svg_wrap, text, line, INK

R = random.Random(61010)
NM = Names(R)
SC = [1000, 2000, 5000, 10000, 20000, 25000, 50000, 100000, 200000, 250000, 500000, 1000000]


def real(cm):
    """公分 → 読みやすい単位"""
    if cm >= 100000 and cm % 100000 == 0:
        return "%s 公里" % num(cm // 100000)
    if cm >= 100000:
        return "%s 公里" % dnum(cm / 100000, 2)
    if cm % 100 == 0:
        return "%s 公尺" % num(cm // 100)
    return "%s 公尺" % dnum(cm / 100, 2)


def s1(seen):
    def mk():
        s = R.choice(SC)
        q = "比例尺 1：%s，表示圖上 1 公分代表實際多少？" % num(s)
        ans = real(s)
        w = ["%s 公尺" % num(s), "%s 公里" % num(s // 1000), "%s 公尺" % num(s // 10)] if s >= 1000 else []
        w = [x for x in w if x != ans]
        if s < 100000:
            w.append("%s 公里" % dnum(s / 1000, 3) if s % 1000 == 0 else real(s * 10))
        return mcq(q, ans, w, "圖上 1 公分是實際 %s 公分 ＝ %s。（100 公分 ＝ 1 公尺，100,000 公分 ＝ 1 公里）" % (num(s), ans))

    def meaning():
        s = R.choice(SC)
        q = "地圖上的比例尺寫著「1：%s」，意思是什麼？" % num(s)
        ans = "圖上距離：實際距離 ＝ 1：%s" % num(s)
        return mcq(q, ans, ["實際距離：圖上距離 ＝ 1：%s" % num(s), "圖上 1 公尺代表實際 %s 公里" % num(s), "地圖放大了 %s 倍" % num(s)],
                   "比例尺是圖上距離和實際距離的比，圖上距離寫在前面。")
    return pick_unique(R, mk, 11, seen) + pick_unique(R, meaning, 9, seen)


def s2(seen):
    def mk():
        s = R.choice(SC)
        d = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 2.5, 3.5, 4.5, 1.5, 12])
        cm = int(d * s)
        q = "比例尺 1：%s 的地圖上，兩地相距 %s 公分。實際距離是多少？" % (num(s), dnum(d))
        ans = real(cm)
        w = [real(cm * 10), real(cm // 10), "%s 公尺" % num(cm)]
        return mcq(q, ans, [x for x in w if x != ans], "%s × %s ＝ %s（公分）＝ %s。" % (dnum(d), num(s), num(cm), ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        s = R.choice(SC)
        d = R.choice([2, 3, 4, 5, 6, 8, 10, 1.5, 2.5, 7.5])
        cm = int(d * s)
        q = "兩地實際相距 %s，畫在比例尺 1：%s 的地圖上，是幾公分？" % (real(cm), num(s))
        return mcq(q, "%s 公分" % dnum(d), ["%s 公分" % dnum(x) for x in (d * 10, d / 10, d * 100)], "先換成公分：%s ＝ %s 公分，%s ÷ %s ＝ %s（公分）。" % (real(cm), num(cm), num(cm), num(s), dnum(d)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def find():
        s = R.choice(SC)
        d = R.choice([2, 3, 4, 5, 8])
        cm = d * s
        q = "地圖上 %d 公分代表實際 %s。這張地圖的比例尺是多少？" % (d, real(cm))
        return mcq(q, "1：%s" % num(s), ["1：%s" % num(x) for x in (cm, s * 10, s // 10)] + ["%s：1" % num(s)], "%s ＝ %s 公分，%s ÷ %d ＝ %s，比例尺 1：%s。" % (real(cm), num(cm), num(cm), d, num(s), num(s)))

    def bar():
        unit = R.choice([(100, "公尺", 10000), (200, "公尺", 20000), (500, "公尺", 50000), (1, "公里", 100000), (2, "公里", 200000), (5, "公里", 500000)])
        W = 240
        s = [line(20, 30, 220, 30, INK, 2)]
        for i in range(5):
            x = 20 + i * 50
            s.append(line(x, 24, x, 36, INK, 2))
            s.append(text(x, 52, str(unit[0] * i), 12))
        s.append(text(232, 52, unit[1], 12, anchor="start"))
        s.append(text(120, 16, "每一格長 1 公分", 11, weight=400))
        g = fig(svg_wrap(W + 40, 62, "".join(s), "線段比例尺"))
        q = "這個線段比例尺，換成數字比例尺是多少？" + g
        return mcq(q, "1：%s" % num(unit[2]), ["1：%s" % num(x) for x in (unit[0], unit[2] * 10, unit[2] // 10)], "1 公分代表 %d %s ＝ %s 公分，比例尺 1：%s。" % (unit[0], unit[1], num(unit[2]), num(unit[2])))
    return pick_unique(R, find, 14, seen) + pick_unique(R, bar, 6, seen)


def s5(seen):
    def walk():
        s = R.choice([10000, 20000, 25000, 50000])
        d = R.choice([3, 4, 5, 6, 8])
        m = d * s // 100
        v = R.choice([50, 60, 80, 100])
        if m % v:
            return None
        who = NM.next()
        q = "%s在比例尺 1：%s 的地圖上量得家到公園 %d 公分。走路的分速是 %d 公尺，要走幾分鐘？" % (who, num(s), d, v)
        return mcq(q, "%d 分鐘" % (m // v), ["%s 分鐘" % num(x) for x in (m * 10 // v, d * v, m // v + 10)], "實際距離 %d × %s ＝ %s 公分 ＝ %s 公尺，%s ÷ %d ＝ %d（分鐘）。" % (d, num(s), num(d * s), num(m), num(m), v, m // v))

    def area():
        s = R.choice([1000, 2000, 5000])
        a, b = R.randint(2, 6), R.randint(2, 6)
        A, B = a * s // 100, b * s // 100
        q = "比例尺 1：%s 的地圖上，一塊長方形農地長 %d 公分、寬 %d 公分。實際長和寬各是幾公尺？" % (num(s), max(a, b), min(a, b))
        ans = "長 %s 公尺、寬 %s 公尺" % (num(max(A, B)), num(min(A, B)))
        return mcq(q, ans, ["長 %s 公尺、寬 %s 公尺" % (num(max(a, b) * s), num(min(a, b) * s)), "長 %s 公尺、寬 %s 公尺" % (num(max(A, B) // 10), num(min(A, B) // 10)), "長 %s 公尺、寬 %s 公尺" % (num(max(A, B) * 10), num(min(A, B) * 10))],
                       "每 1 公分代表 %s 公尺：%d × %s ＝ %s，%d × %s ＝ %s。" % (num(s // 100), max(a, b), num(s // 100), num(max(A, B)), min(a, b), num(s // 100), num(min(A, B))))

    def which():
        s1_, s2_ = R.sample([10000, 50000, 100000, 500000, 1000000], 2)
        q = "兩張地圖的比例尺是 1：%s 和 1：%s。同一個公園，畫在哪一張地圖上比較大？" % (num(s1_), num(s2_))
        ans = "1：%s" % num(min(s1_, s2_))
        return mcq(q, ans, ["1：%s" % num(max(s1_, s2_)), "一樣大", "要看紙的大小"], "1 公分代表的實際距離越短，地圖畫得越詳細，公園看起來越大：%s。" % ans)
    return pick_unique(R, walk, 7, seen) + pick_unique(R, area, 7, seen) + pick_unique(R, which, 6, seen)


def main():
    seen = set()
    sets = [("比例尺的意思", s1(seen)), ("圖上距離求實際距離", s2(seen)), ("實際距離求圖上距離", s3(seen)),
            ("求比例尺", s4(seen)), ("應用", s5(seen))]
    body = lesson(
        ["<b>比例尺 ＝ 圖上距離：實際距離</b>。1：10,000 表示圖上 1 公分代表實際 10,000 公分 ＝ 100 公尺。",
         "實際距離 ＝ 圖上距離 × 比例尺後項；圖上距離 ＝ 實際距離 ÷ 比例尺後項（先換成公分）。",
         "記住：100 公分 ＝ 1 公尺，100,000 公分 ＝ 1 公里。"],
        [example("比例尺 1：50,000，圖上 4 公分是實際多遠？", ["4 × 50,000 ＝ 200,000（公分）。", "200,000 公分 ＝ 2 公里。"], "2 公里"),
         example("實際 3 公里，畫在 1：100,000 的地圖上幾公分？", ["3 公里 ＝ 300,000 公分。", "300,000 ÷ 100,000 ＝ 3。"], "3 公分")],
        [("1：10,000 的 1 公分代表 10,000 公尺", "是 10,000 公分 ＝ 100 公尺"),
         ("求圖上距離用乘法", "要用除法，先換成公分"),
         ("比例尺後項越大，地圖上東西越大", "後項越大，東西畫得越小")])
    faq = [{"q": "比例尺 1：25,000 是什麼意思？",
            "a": "圖上距離和實際距離的比是 1：25,000，圖上 1 公分代表實際 25,000 公分，也就是 250 公尺。"},
           {"q": "什麼是線段比例尺？",
            "a": "用一條分格的線段標出每一格代表的實際距離，例如每 1 公分代表 1 公里，換成數字比例尺是 1：100,000。"},
           {"q": "六年級的比例尺要學什麼？",
            "a": "108課綱 S-6-2：地圖比例尺的意義、記號與應用，知道地圖上兩邊長的比和實際兩邊長的比相等。"}]
    make_unit(R, "grade-6", "map-scales", "S-6-2",
              "解題：地圖比例尺。地圖比例尺之意義、記號與應用。地圖上兩邊長的比和實際兩邊長的比相等。",
              "地圖比例尺",
              "六年級數學 比例尺 練習題｜圖上距離・實際距離・線段比例尺 學習單（附解答）",
              "地圖比例尺",
              "國小六年級數學「地圖比例尺」免費學習單：比例尺的意思、圖上距離和實際距離的換算、求比例尺、線段比例尺與走路時間、農地大小等應用題。100題線上練習馬上對答案，附可列印解答。",
              "比例尺 ＝ 圖上距離：實際距離",
              "圖上 1 公分代表實際多少公分，再換成公尺或公里。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
