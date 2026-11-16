# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：數量模式與推理（108課綱 R-3-2）
  python3 tools/gen_tw_math_g3_patterns.py
數列（每次加・減同じ数）、空格、重複的圖形模式（第 n 個）、成長的圖形（火柴棒）、一維表格（桌子と座位、日曆）。
誤答：差を1つ数え間違える、第 n 個を n×差 とする（初項を忘れる）、周期の余りの扱い。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, table, GREEN, FILL, INK, RED, BLUE

R = random.Random(31023)
NM = Names(R)


def s1(seen):
    def mk():
        d = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25, 50, 100])
        a = R.randint(1, 60) if d < 20 else R.randint(1, 20) * 5
        seq = [a + d * i for i in range(5)]
        nxt = a + d * 5
        q = "依照規律，下一個數是多少？ %s，___" % "，".join(num(x) for x in seq)
        return mcq(q, num(nxt), [num(x) for x in (nxt + d, nxt - 1, nxt + 1, seq[-1] + d + 10 if d != 10 else nxt + 5)],
                   "每次加 %d：%s ＋ %d ＝ %s。" % (d, num(seq[-1]), d, num(nxt)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def down():
        d = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50])
        a = d * R.randint(8, 20) + R.randint(0, d - 1)
        seq = [a - d * i for i in range(5)]
        nxt = a - d * 5
        if nxt < 0:
            return None
        q = "依照規律，下一個數是多少？ %s，___" % "，".join(num(x) for x in seq)
        return mcq(q, num(nxt), [num(x) for x in (nxt - d, nxt + 1, nxt - 1, seq[-1] + d)], "每次減 %d：%s － %d ＝ %s。" % (d, num(seq[-1]), d, num(nxt)))

    def gap():
        d = R.choice([3, 4, 5, 6, 7, 8, 9, 11, 12, 15])
        a = R.randint(2, 50)
        seq = [a + d * i for i in range(6)]
        k = R.randint(1, 4)
        shown = [num(x) if i != k else "___" for i, x in enumerate(seq)]
        q = "空格裡要填什麼數？ %s" % "，".join(shown)
        v = seq[k]
        return mcq(q, num(v), [num(x) for x in (v + 1, v - 1, v + d, seq[k - 1] + 10 if d != 10 else v + 2)],
                   "相鄰兩數相差 %d：%s ＋ %d ＝ %s。" % (d, num(seq[k - 1]), d, num(v)))

    def rule():
        d = R.choice([3, 4, 6, 7, 8, 9, 12])
        up = R.random() < .6
        a = R.randint(5, 40) if up else d * 10 + R.randint(0, 9)
        seq = [a + d * i if up else a - d * i for i in range(5)]
        q = "這組數的規律是什麼？ %s" % "，".join(num(x) for x in seq)
        ans = "每次%s %d" % ("加" if up else "減", d)
        return mcq(q, ans, ["每次%s %d" % ("減" if up else "加", d), "每次%s %d" % ("加" if up else "減", d + 1), "每次%s %d" % ("加" if up else "減", d - 1)],
                   "相鄰兩數相差 %d，%s，所以是每次%s %d。" % (d, "越來越大" if up else "越來越小", "加" if up else "減", d))
    return pick_unique(R, down, 7, seen) + pick_unique(R, gap, 7, seen) + pick_unique(R, rule, 6, seen)


SH = ["circle", "tri", "square", "star"]
COL = {"circle": RED, "tri": BLUE, "square": GREEN, "star": "#d08a00"}
NAME = {"circle": "●", "tri": "▲", "square": "■", "star": "★"}
ZH = {"circle": "圓形", "tri": "三角形", "square": "正方形", "star": "星形"}


def shape(k, x, y):
    c = COL[k]
    if k == "circle":
        return "<circle cx='%d' cy='%d' r='11' fill='%s'/>" % (x, y, c)
    if k == "tri":
        return "<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (x, y - 12, x - 12, y + 10, x + 12, y + 10, c)
    if k == "square":
        return "<rect x='%d' y='%d' width='22' height='22' fill='%s'/>" % (x - 11, y - 11, c)
    return "<polygon points='%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d' fill='%s'/>" % (
        x, y - 13, x + 4, y - 4, x + 13, y - 4, x + 6, y + 3, x + 9, y + 12, x, y + 7, x - 9, y + 12, x - 6, y + 3, x - 13, y - 4, x - 4, y - 4, c)


def s3(seen):
    def mk():
        L = R.randint(2, 4)
        unit = R.sample(SH, L) if R.random() < .6 else (lambda u: u)([R.choice(SH) for _ in range(L)])
        if len(set(unit)) < 2:
            return None
        show = (unit * 6)[:max(2 * L + 2, 8)]
        n = R.randint(15, 40)
        k = unit[(n - 1) % L]
        body = "".join(shape(s, 20 + i * 32, 22) for i, s in enumerate(show)) + text(20 + len(show) * 32, 28, "……", 16)
        q = "圖形依照規律排列，第 %d 個是什麼？" % n + fig(svg_wrap(20 + len(show) * 32 + 40, 44, body, "重複排列的圖形"))
        r = n % L
        opts = [ZH[x] for x in SH if ZH[x] != ZH[k]]
        return mcq(q, ZH[k], opts, "每 %d 個重複一次。%d ÷ %d ＝ %d……%d，%s，所以第 %d 個是%s。" % (
            L, n, L, n // L, r, "餘 %d 就是一組裡的第 %d 個" % (r, r) if r else "沒有餘數就是一組的最後一個", n, ZH[k]))
    return pick_unique(R, mk, 20, seen)


def sticks_svg(kind, n):
    """kind：'sq' 正方形を横に並べる（3k+1 本）、'tri' 三角形（2k+1 本）"""
    s = []
    x0 = 10
    for k in range(1, n + 1):
        w = 0
        if kind == "sq":
            for i in range(k):
                x = x0 + i * 22
                s += [line(x, 30, x + 22, 30, INK, 3), line(x, 52, x + 22, 52, INK, 3), line(x, 30, x, 52, INK, 3)]
            s.append(line(x0 + k * 22, 30, x0 + k * 22, 52, INK, 3))
            w = k * 22
        else:
            P = [(x0 + 13 * j, 52 if j % 2 == 0 else 30) for j in range(k + 2)]   # 上下交互に k 個の三角形（2k+1 本）
            for j in range(k + 1):
                s.append(line(P[j][0], P[j][1], P[j + 1][0], P[j + 1][1], INK, 3))
            for i in range(k):
                s.append(line(P[i][0], P[i][1], P[i + 2][0], P[i + 2][1], INK, 3))
            w = 13 * (k + 1)
        s.append(text(x0 + w / 2, 72, "第 %d 個" % k, 12))
        x0 += w + 34
    return fig(svg_wrap(int(x0), 80, "".join(s), "火柴棒排出的圖形"))


def s4(seen):
    def mk():
        kind = R.choice(["sq", "tri"])
        n = R.randint(4, 15)
        per, base = (3, 1) if kind == "sq" else (2, 1)
        v = per * n + base
        q = "用火柴棒排圖形，照這樣排下去，第 %d 個要用幾根火柴棒？" % n + sticks_svg(kind, 3)
        return mcq(q, "%d 根" % v, ["%d 根" % x for x in (per * n, (per + 1) * n, v + per, v - 1, v + 1, v - per)],
                   "第 1 個用 %d 根，之後每多一個%s多 %d 根：%d ＋ %d × %d ＝ %d（根）。" % (
                       per + base, "正方形" if kind == "sq" else "三角形", per, per + base, per, n - 1, v))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def seats():
        n = R.randint(5, 12)
        q = "長方形桌子併成一排，桌子和座位的關係如下表。%d 張桌子有幾個座位？" % n + table(
            ["桌子（張）", "1", "2", "3", "4", "…", str(n)], [["座位（個）", "6", "10", "14", "18", "…", "？"]])
        v = 4 * n + 2
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (6 * n, 4 * n, v + 4, v - 2)], "每多 1 張桌子多 4 個座位：6 ＋ 4 × %d ＝ %d（個）。" % (n - 1, v))

    def cal():
        d = R.randint(1, 9)
        k = R.randint(2, 3)
        q = "這個月 %d 日是星期三，再過 %d 個星期的星期三是幾日？" % (d, k)
        v = d + 7 * k
        return mcq(q, "%d 日" % v, ["%d 日" % x for x in (d + k, d + 7, v + 1, d + 5 * k)], "每過 1 個星期多 7 天：%d ＋ 7 × %d ＝ %d（日）。" % (d, k, v))

    def save():
        who = NM.next()
        a, d = R.randint(10, 50), R.choice([5, 10, 15, 20])
        n = R.randint(5, 10)
        q = "%s的撲滿第 1 週有 %d 元，以後每週多存 %d 元。第 %d 週撲滿裡有多少元？" % (who, a, d, n)
        v = a + d * (n - 1)
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (a + d * n, d * n, a * n, v - d - 1)], "%d ＋ %d × %d ＝ %d（元）。（第 1 週之後又過了 %d 週）" % (a, d, n - 1, v, n - 1))
    return pick_unique(R, seats, 6, seen) + pick_unique(R, cal, 7, seen) + pick_unique(R, save, 7, seen)


def main():
    seen = set()
    sets = [("找下一個數", s1(seen)), ("減少的數列和空格", s2(seen)), ("重複的圖形", s3(seen)),
            ("火柴棒的圖形", s4(seen)), ("生活中的規律", s5(seen))]
    body = lesson(
        ["找規律：看相鄰的兩個數<b>差多少</b>，是每次加還是每次減。",
         "重複的圖形：先找<b>幾個一組</b>，再用除法看第幾個落在一組的哪一個位置。",
         "成長的圖形：第 1 個之後，<b>每多一個加多少</b>，第 n 個 ＝ 第 1 個 ＋ 每次增加的數 ×（n － 1）。"],
        [example("5，9，13，17，___", ["相差 4，每次加 4。", "17 ＋ 4 ＝ 21。"], "21"),
         example("●▲■●▲■……，第 20 個是什麼？", ["3 個一組。20 ÷ 3 ＝ 6……2。", "餘 2，是一組裡的第 2 個。"], "▲（三角形）")],
        [("第 n 個 ＝ 每次增加的數 × n", "別忘了第 1 個的數：第 1 個 ＋ 增加 ×（n － 1）"),
         ("沒有餘數時說是一組的第 1 個", "沒有餘數是一組的最後一個"),
         ("只看前兩個數就決定規律", "多看幾個，確定每次都一樣")])
    faq = [{"q": "三年級的「數量模式」要學什麼？",
            "a": "108課綱 R-3-2：觀察數列、圖形和一維圖表的變化，找出規律並推理下一個或第幾個，以操作活動為主。"},
           {"q": "孩子看不出數列的規律，怎麼辦？",
            "a": "在每兩個數中間寫出「＋幾」或「－幾」，常常一眼就看出每次加或減的數一樣。"},
           {"q": "重複圖形的第幾個要怎麼算？",
            "a": "先數幾個一組，用除法：位置 ÷ 一組的個數，看餘數。餘 1 是第 1 個，沒有餘數是最後一個。"}]
    make_unit(R, "grade-3", "patterns", "R-3-2",
              "數量模式與推理（I）：以操作活動為主。一維變化模式之觀察與推理，例如數列、一維圖表等。",
              "數量模式與推理：數列和圖形的規律",
              "三年級數學 找規律 練習題｜數列・重複圖形・火柴棒 學習單（附解答）",
              "數量模式與規律",
              "國小三年級數學「找規律」免費學習單：數列的下一個數、填空格、重複的圖形第幾個、火柴棒圖形、桌子座位和日曆的規律。100題線上練習馬上對答案，附可列印解答。",
              "看相鄰兩數差多少",
              "重複的圖形用除法看餘數；成長的圖形看每次增加多少。",
              body, faq, sets, 22)


if __name__ == "__main__":
    main()
