# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：線對稱（108課綱 S-5-4）
  python3 tools/gen_tw_math_g5_line_symmetry.py
對稱軸の数（特殊な図形）、方格紙で對稱點を求める、對稱邊・對稱角は等しい、對稱軸と對稱點を結ぶ線は垂直、線對稱かどうか（文字・図形）、推理。
誤答：平行四邊形を線對稱とする、長方形の對角線を對稱軸とする、對稱點を軸から同じ方向に取る。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK, RED, BLUE

R = random.Random(51020)
NM = Names(R)
LET = "甲乙丙丁"
AXES = [("正方形", "4 條"), ("長方形（不是正方形）", "2 條"), ("正三角形", "3 條"), ("等腰三角形（不是正三角形）", "1 條"), ("菱形（不是正方形）", "2 條"),
        ("等腰梯形", "1 條"), ("平行四邊形（不是長方形、菱形）", "0 條（不是線對稱圖形）"), ("正五邊形", "5 條"), ("正六邊形", "6 條"), ("圓", "無限多條"),
        ("半圓", "1 條"), ("一般的三角形（三邊都不一樣長）", "0 條（不是線對稱圖形）")]


def s1(seen):
    out = []
    opts = ["0 條（不是線對稱圖形）", "1 條", "2 條", "3 條", "4 條", "5 條", "6 條", "無限多條"]
    for name, ans in AXES:
        w = [o for o in opts if o != ans]
        R.shuffle(w)
        if name.startswith("長方形"):
            w = ["4 條"] + [o for o in w if o != "4 條"]
        out.append(mcq("%s有幾條對稱軸？" % name, ans, w, "%s有 %s對稱軸。%s" % (name, ans.replace("（不是線對稱圖形）", ""), "（對角線不是長方形的對稱軸，沿對角線摺不會重合）" if name.startswith("長方形") else "")))
    for o in out:
        seen.add(o["q"])

    def which():
        good = R.choice(["正方形", "等腰梯形", "菱形", "正三角形", "圓", "等腰三角形", "長方形"])
        bads = R.sample(["平行四邊形", "一般的三角形", "一般的梯形", "不等邊的四邊形"], 3)
        return mcq("下面哪一個<b>是</b>線對稱圖形？", good, bads, "沿著對稱軸摺起來兩邊會完全重合：%s是線對稱圖形；平行四邊形、一般的三角形和梯形都不是。" % good) if False else None
    return out + [mcq("下面哪一個<b>是</b>線對稱圖形？（%s）" % k, g, b, "沿對稱軸對摺，兩邊完全重合的才是線對稱圖形：%s。" % g)
                  for k, g, b in [("一", "等腰梯形", ["平行四邊形", "一般的三角形", "一般的梯形"]), ("二", "菱形", ["平行四邊形", "一般的梯形", "不等邊的四邊形"]),
                                  ("三", "正三角形", ["一般的三角形", "平行四邊形", "不等邊的四邊形"]), ("四", "圓", ["平行四邊形", "一般的梯形", "一般的三角形"]),
                                  ("五", "長方形", ["平行四邊形", "一般的三角形", "不等邊的四邊形"]), ("六", "等腰三角形", ["一般的三角形", "一般的梯形", "平行四邊形"]),
                                  ("七", "正六邊形", ["平行四邊形", "一般的三角形", "一般的梯形"]), ("八", "半圓", ["平行四邊形", "一般的梯形", "不等邊的四邊形"])]]


def grid_point(ax, px, py, cols=10, rows=7):
    C = 26
    s = []
    for i in range(cols + 1):
        s.append(line(10 + i * C, 10, 10 + i * C, 10 + rows * C, "#ddd", 1))
    for j in range(rows + 1):
        s.append(line(10, 10 + j * C, 10 + cols * C, 10 + j * C, "#ddd", 1))
    s.append(line(10 + ax * C, 4, 10 + ax * C, 16 + rows * C, BLUE, 2.5, " stroke-dasharray='6 4'"))
    s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (10 + px * C, 10 + py * C, RED))
    s.append(text(10 + px * C, 10 + py * C - 10, "A", 14, col=RED))
    for k, lab in enumerate("甲乙丙丁"):
        pass
    return s, C


def s2(seen):
    def mk():
        ax = R.randint(3, 7)
        px = ax - R.randint(1, 3) if R.random() < .5 else ax + R.randint(1, 3)
        py = R.randint(1, 6)
        if not (0 <= px <= 10):
            return None
        tx = 2 * ax - px
        if not (0 <= tx <= 10):
            return None
        s, C = grid_point(ax, px, py)
        cand = [(tx, py), (px + (ax - px) // abs(ax - px) * 1 if px != ax else px, py) if False else (ax + (ax - px) + (1 if tx > ax else -1), py), (tx, py + 1 if py < 6 else py - 1), (ax, py)]
        cand = [(x, y) for x, y in cand if 0 <= x <= 10 and 0 <= y <= 7]
        uniq = []
        for c in cand:
            if c not in uniq:
                uniq.append(c)
        if len(uniq) < 4 or uniq[0] != (tx, py):
            return None
        R.shuffle(uniq)
        k = uniq.index((tx, py))
        for i, (x, y) in enumerate(uniq):
            s.append("<circle cx='%d' cy='%d' r='5' fill='#fff' stroke='%s' stroke-width='2'/>" % (10 + x * C, 10 + y * C, GREEN))
            s.append(text(10 + x * C + 12, 10 + y * C + 16, LET[i], 12, col=GREEN))
        q = "藍色虛線是對稱軸，A 的對稱點是哪一個？" + fig(svg_wrap(10 * C + 30, 7 * C + 30, "".join(s), "方格紙上的對稱軸和點"))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "對稱點在對稱軸的另一邊，和對稱軸的距離一樣（%d 格），而且在同一條橫線上：%s。" % (abs(ax - px), LET[k]))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def side():
        a = R.randint(3, 15)
        q = "線對稱圖形中，邊 AB 的對稱邊是 CD，AB ＝ %d 公分，CD 是幾公分？" % a
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (a * 2, a // 2 if a > 2 else a + 2, a + 1)], "對稱邊一樣長：%d 公分。" % a)

    def ang():
        a = R.randint(30, 150)
        q = "線對稱圖形中，∠A 的對稱角是 ∠D，∠A ＝ %d 度，∠D 是幾度？" % a
        return mcq(q, "%d 度" % a, ["%d 度" % x for x in (180 - a if 180 - a != a else a + 10, 360 - a, 90)], "對稱角一樣大：%d 度。" % a)

    def dist():
        d = R.randint(2, 12)
        q = "點 P 到對稱軸的距離是 %d 公分，P 和它的對稱點 Q 相距幾公分？" % d
        return mcq(q, "%d 公分" % (2 * d), ["%d 公分" % x for x in (d, d + 2, d * 4)], "Q 在另一邊，也距離 %d 公分：%d × 2 ＝ %d（公分）。" % (d, d, 2 * d))

    def perp():
        F = [("連接兩個對稱點的線段，和對稱軸有什麼關係？", "互相垂直", ["互相平行", "一樣長", "沒有關係"], "對稱點的連線和對稱軸垂直，而且被對稱軸平分。"),
             ("對稱軸會把對稱點的連線分成怎樣的兩段？", "一樣長的兩段", ["一長一短", "三段", "不一定"], "對稱軸平分對稱點的連線。"),
             ("等腰三角形的對稱軸經過哪裡？", "頂點和底邊的中點", ["兩個底角", "底邊的一端", "三角形外面"], "等腰三角形的對稱軸從頂點垂直通過底邊中點。")]
        return mcq(*R.choice(F))
    return pick_unique(R, side, 6, seen) + pick_unique(R, ang, 6, seen) + pick_unique(R, dist, 5, seen) + pick_unique(R, perp, 3, seen)


def s4(seen):
    SYM = ["A", "H", "M", "O", "T", "U", "V", "W", "X", "Y", "B", "C", "D", "E"]
    NO = ["F", "G", "J", "L", "N", "P", "Q", "R", "S", "Z"]

    def mk():
        g = R.choice(SYM)
        bs = R.sample(NO, 3)
        L = bs + [g]
        R.shuffle(L)
        return mcq("%s 這幾個大寫英文字母中，哪一個是線對稱圖形？" % "、".join(L), g, bs, "%s 沿著一條直線對摺可以完全重合；%s 都不能。" % (g, "、".join(bs)))

    def zh():
        G = ["中", "日", "田", "木", "山", "王", "十", "工", "土", "大", "米", "口"]
        Nn = ["不", "火", "小", "水", "女", "子", "多", "七", "九", "乃"]
        g = R.choice(G)
        bs = R.sample(Nn, 3)
        L = bs + [g]
        R.shuffle(L)
        return mcq("「%s」這幾個字（用正楷寫）中，哪一個可以看成線對稱圖形？" % "、".join(L), g, bs, "「%s」左右兩邊對摺可以重合，是線對稱的。" % g)
    return pick_unique(R, mk, 12, seen) + pick_unique(R, zh, 8, seen)


def s5(seen):
    def fold():
        w = R.randint(5, 14)
        h = R.randint(2, w - 2)
        q = "把一張紙對摺，剪下一個長 %d 公分、寬 %d 公分的長方形（摺線是長的那一邊），打開後的圖形周長是幾公分？" % (w, h)
        W = 2 * h
        P = 2 * (w + W)
        return mcq(q, "%d 公分" % P, ["%d 公分" % x for x in (2 * (w + h), 2 * w + 2 * h + h, P // 2 + w)], "打開後長 %d、寬 %d × 2 ＝ %d，周長（%d ＋ %d）× 2 ＝ %d（公分）。" % (w, h, W, w, W, P))

    def half_area():
        A = R.randint(10, 80)
        q = "一個線對稱圖形，對稱軸一邊的面積是 %d 平方公分，整個圖形的面積是多少？" % A
        return mcq(q, "%d 平方公分" % (2 * A), ["%d 平方公分" % x for x in (A, A + 2, A * 4)], "兩邊一模一樣：%d × 2 ＝ %d（平方公分）。" % (A, 2 * A))

    def axis_count():
        F = [("正方形和長方形的對稱軸一共差幾條？", "2 條", ["1 條", "0 條", "4 條"], "正方形 4 條，長方形 2 條，差 2 條。"),
             ("正方形的對稱軸會經過哪裡？", "對邊的中點，或兩個相對的頂點", ["只經過頂點", "只經過邊的中點", "不經過圖形"], "正方形有 4 條對稱軸：2 條連對邊中點，2 條是對角線。"),
             ("長方形的對角線是不是對稱軸？", "不是", ["是", "只有一條是", "要看大小"], "沿長方形的對角線摺，兩邊不會完全重合。"),
             ("菱形的對稱軸是哪兩條線？", "兩條對角線", ["兩組對邊的中點連線", "四條邊", "沒有對稱軸"], "菱形沿對角線對摺會完全重合。")]
        return mcq(*R.choice(F))
    return pick_unique(R, fold, 8, seen) + pick_unique(R, half_area, 8, seen) + pick_unique(R, axis_count, 4, seen)


def main():
    seen = set()
    sets = [("對稱軸有幾條", s1(seen)), ("找對稱點", s2(seen)), ("對稱邊、對稱角", s3(seen)), ("字母和國字", s4(seen)), ("推理和應用", s5(seen))]
    body = lesson(
        ["沿著一條直線對摺，兩邊能<b>完全重合</b>的圖形叫<b>線對稱圖形</b>，那條直線叫<b>對稱軸</b>。",
         "重合的點、邊、角叫對稱點、對稱邊、對稱角：<b>對稱邊一樣長，對稱角一樣大</b>。",
         "對稱點的連線和對稱軸<b>垂直</b>，而且被對稱軸<b>平分</b>（兩邊到軸的距離一樣）。",
         "正方形 4 條、長方形 2 條、正三角形 3 條、等腰三角形 1 條、圓有無限多條；平行四邊形不是線對稱圖形。"],
        [example("點 A 在對稱軸左邊 3 格，對稱點在哪裡？", ["在對稱軸右邊 3 格，同一條橫線上。"], "右邊 3 格"),
         example("長方形有幾條對稱軸？", ["上下對摺、左右對摺都會重合；沿對角線不會。"], "2 條")],
        [("長方形的對角線是對稱軸", "沿對角線摺不會重合，長方形只有 2 條"),
         ("平行四邊形是線對稱圖形", "找不到能對摺重合的線"),
         ("對稱點畫在對稱軸的同一邊", "要在另一邊，距離一樣")])
    faq = [{"q": "什麼是線對稱圖形？",
            "a": "沿著一條直線對摺後兩邊能完全重合的圖形，這條直線是對稱軸。"},
           {"q": "常見圖形有幾條對稱軸？",
            "a": "正方形 4 條、長方形 2 條、菱形 2 條、正三角形 3 條、等腰三角形 1 條、等腰梯形 1 條、圓有無限多條；平行四邊形沒有。"},
           {"q": "五年級的線對稱要學什麼？",
            "a": "108課綱 S-5-4：線對稱的意義和對稱軸、對稱點、對稱邊、對稱角，知道特殊圖形的線對稱性質，並製作線對稱圖形。"}]
    make_unit(R, "grade-5", "line-symmetry", "S-5-4",
              "線對稱：線對稱的意義。「對稱軸」、「對稱點」、「對稱邊」、「對稱角」。由操作活動知道特殊平面圖形的線對稱性質。利用線對稱做簡單幾何推理。製作或繪製線對稱圖形。",
              "線對稱：對稱軸、對稱點",
              "五年級數學 線對稱 練習題｜對稱軸・對稱點・對稱圖形 學習單（附解答）",
              "線對稱",
              "國小五年級數學「線對稱」免費學習單：常見圖形有幾條對稱軸、在方格紙上找對稱點、對稱邊和對稱角、對稱的字母和國字與推理應用。100題線上練習馬上對答案，附可列印解答。",
              "對摺後完全重合，就是線對稱",
              "對稱邊一樣長、對稱角一樣大；對稱點到軸的距離一樣。",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
