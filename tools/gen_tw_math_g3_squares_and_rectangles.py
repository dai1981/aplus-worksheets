# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：正方形和長方形（108課綱 S-3-2）
  python3 tools/gen_tw_math_g3_squares_and_rectangles.py
邊と角の特徴で正方形・長方形を見分ける、性質の正誤、邊長、四條邊的總長、生活の問題。
誤答：菱形を正方形と思う（角を見ない）、平行四邊形を長方形と思う、正方形は長方形ではないと思う。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK, RED

R = random.Random(31018)
NM = Names(R)
LET = "甲乙丙丁"


def quad(kind, x, y, s):
    """kind の四角形の頂点（幅 s 前後の枠に収める）"""
    if kind == "square":
        a = s * R.choice([.7, .8, .9])
        return [(x, y), (x + a, y), (x + a, y + a), (x, y + a)]
    if kind == "rect":
        w, h = s * R.choice([.9, 1]), s * R.choice([.45, .55, .6])
        return [(x, y + 10), (x + w, y + 10), (x + w, y + 10 + h), (x, y + 10 + h)]
    if kind == "rhombus":
        a = s * .45
        return [(x + a, y), (x + 2 * a, y + a * .75), (x + a, y + 1.5 * a), (x, y + a * .75)]
    if kind == "para":
        o = s * .25
        return [(x + o, y + 10), (x + s, y + 10), (x + s - o, y + 10 + s * .55), (x, y + 10 + s * .55)]
    o = s * .2   # trapezoid
    return [(x + o, y + 10), (x + s - o * 1.5, y + 10), (x + s, y + 10 + s * .55), (x, y + 10 + s * .55)]


def four_svg(kinds):
    s = []
    for i, k in enumerate(kinds):
        x = 14 + i * 120
        pts = quad(k, x, 30, 96)
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN))
        s.append(text(x + 45, 22, LET[i], 17))
    return fig(svg_wrap(490, 140, "".join(s), "甲乙丙丁四個四邊形"))


def rect_svg(w, h, lab_top, lab_left, ask=None):
    sc = min(260 / w, 150 / h, 16)
    W, H = w * sc, h * sc
    s = ["<rect x='80' y='30' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='3'/>" % (W, H, FILL, GREEN)]
    s.append(text(80 + W / 2, 22, lab_top, 15))
    s.append(text(72, 30 + H / 2 + 5, lab_left, 15, anchor="end"))
    if ask:
        s.append(text(80 + W / 2, 30 + H + 22, "?", 18, col=RED))
    return fig(svg_wrap(int(W + 100), int(H + 60), "".join(s), "長方形"))


def s1(seen):
    NAME = {"square": "正方形", "rect": "長方形", "rhombus": "菱形", "para": "平行四邊形", "trap": "梯形"}

    def mk():
        target = R.choice(["square", "rect"])
        others = R.sample([k for k in ("rhombus", "para", "trap", "square", "rect") if k != target], 3)
        if target == "rect" and "square" in others:
            others.remove("square")
            others.append(R.choice(["rhombus", "para", "trap"]))
            if len(set(others)) < 3:
                return None
        kinds = others + [target]
        R.shuffle(kinds)
        ans = LET[kinds.index(target)]
        q = "哪一個是%s？" % NAME[target] + four_svg(kinds)
        trap_let = [LET[i] for i, k in enumerate(kinds) if k in ("rhombus", "para")]
        e = ("正方形：4 條邊一樣長，4 個角都是直角。" if target == "square" else "長方形：4 個角都是直角，對邊一樣長。")
        if trap_let:
            e += "%s的角不是直角，所以不是。" % "、".join(trap_let)
        return mcq(q, ans, [l for l in LET if l != ans], e)
    return pick_unique(R, mk, 20, seen)


TRUE = ["正方形的 4 條邊都一樣長。", "正方形的 4 個角都是直角。", "長方形的 4 個角都是直角。", "長方形相對的兩條邊一樣長。",
        "正方形也是一種長方形。", "長方形有 4 條邊、4 個角。", "把正方形上下對摺，兩半會完全疊合。"]
FALSE = ["長方形的 4 條邊都一樣長。", "4 條邊一樣長的四邊形一定是正方形。", "正方形只有 2 個直角。", "長方形相鄰的兩條邊一定一樣長。",
         "斜放的正方形就不是正方形了。", "4 個角都是直角的四邊形一定是正方形。", "正方形和長方形都只有 3 個角。", "長方形的 4 個角有大有小。"]


def s2(seen):
    def mk():
        ask_true = R.random() < .5
        if ask_true:
            ans, ws, word = R.choice(TRUE), R.sample(FALSE, 3), "對"
        else:
            ans, ws, word = R.choice(FALSE), R.sample(TRUE, 3), "錯"
        st = ws + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % (word, "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s%s" % (LET[k], ans, EXPL.get(ans, "正方形：4 邊等長、4 個直角。長方形：4 個直角、對邊等長。")))
    return pick_unique(R, mk, 20, seen)


EXPL = {
    "4 條邊一樣長的四邊形一定是正方形。": "還要 4 個角都是直角才是正方形（菱形 4 邊等長，但角不是直角）。",
    "4 個角都是直角的四邊形一定是正方形。": "4 個直角的四邊形是長方形；4 條邊也一樣長才是正方形。",
    "長方形的 4 條邊都一樣長。": "長方形是相對的兩條邊一樣長。",
    "斜放的正方形就不是正方形了。": "轉個方向，邊和角都沒變，還是正方形。",
    "正方形也是一種長方形。": "正方形 4 個角都是直角、對邊等長，符合長方形的特徵，所以是特別的長方形。",
}


def s3(seen):
    def rect():
        w, h = R.randint(6, 24), R.randint(3, 15)
        if w <= h + 1:
            return None
        q = "長方形的長是 %d 公分，寬是 %d 公分。下面「?」的邊長幾公分？" % (w, h) + rect_svg(w, h, "%d 公分" % w, "%d 公分" % h, True)
        return mcq(q, "%d 公分" % w, ["%d 公分" % x for x in (h, w + h, w - h, 2 * w)], "長方形相對的兩條邊一樣長，下面的邊和上面一樣是 %d 公分。" % w)

    def sq():
        a = R.randint(3, 20)
        q = "正方形的一條邊長 %d 公分，另外 3 條邊各長幾公分？" % a
        return mcq(q, "都是 %d 公分" % a, ["都是 %d 公分" % (a * 2), "都是 %d 公分" % (a * 4), "不一定"], "正方形 4 條邊都一樣長，都是 %d 公分。" % a)
    return pick_unique(R, rect, 12, seen) + pick_unique(R, sq, 8, seen)


def s4(seen):
    def rect_total():
        w, h = R.randint(5, 30), R.randint(2, 20)
        if w <= h:
            return None
        t = 2 * (w + h)
        q = "長方形的長 %d 公分、寬 %d 公分，4 條邊一共長幾公分？" % (w, h)
        return mcq(q, "%d 公分" % t, ["%d 公分" % x for x in (w + h, w * h, 2 * w + h, 4 * w)], "長 2 條、寬 2 條：%d ＋ %d ＋ %d ＋ %d ＝ %d（公分）。" % (w, w, h, h, t))

    def sq_total():
        a = R.randint(3, 25)
        q = "正方形的一條邊長 %d 公分，4 條邊一共長幾公分？" % a
        return mcq(q, "%d 公分" % (4 * a), ["%d 公分" % x for x in (2 * a, a * a if a * a != 4 * a else a + 4, a + 4, 3 * a)], "4 條邊一樣長：%d × 4 ＝ %d（公分）。" % (a, 4 * a))

    def sq_back():
        a = R.randint(3, 15)
        q = "用一條 %d 公分長的鐵絲剛好圍成一個正方形，正方形的一條邊長幾公分？" % (4 * a)
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (2 * a, 4 * a, a + 2, a * 4 - 4)], "正方形有 4 條一樣長的邊：%d ÷ 4 ＝ %d（公分）。" % (4 * a, a))
    return pick_unique(R, rect_total, 8, seen) + pick_unique(R, sq_total, 6, seen) + pick_unique(R, sq_back, 6, seen)


def s5(seen):
    def cut():
        w, h = R.randint(10, 30), R.randint(5, 20)
        if w <= h:
            return None
        q = "從一張長 %d 公分、寬 %d 公分的長方形紙，剪下一個最大的正方形，正方形的邊長是幾公分？" % (w, h)
        return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (w, w - h if w - h != h else w + h, w + h)], "正方形的邊不能比紙的寬還長，最大是 %d 公分。" % h)

    def left():
        w, h = R.randint(10, 30), R.randint(5, 20)
        if w <= h + 1 or w == 2 * h:
            return None
        q = "長 %d 公分、寬 %d 公分的長方形紙，剪下邊長 %d 公分的正方形後，剩下的長方形長和寬是多少？" % (w, h, h)
        return mcq(q, "長 %d 公分、寬 %d 公分" % (max(w - h, h), min(w - h, h)) if w - h != h else "邊長 %d 公分的正方形" % h,
                   ["長 %d 公分、寬 %d 公分" % x for x in ((w, max(w - h, 1)) if w - h < w else (w, h), (max(w - h, h), max(w - h, h)), (w + h, h), (w, h))],
                   "剩下的一邊是 %d － %d ＝ %d 公分，另一邊還是 %d 公分。" % (w, h, w - h, h))

    def tiles():
        a = R.randint(2, 5)
        n = R.randint(2, 5)
        if a == n:
            return None
        who = NM.next()
        q = "%s用邊長 %d 公分的正方形卡片排成一排，排了 %d 張，拼成一個長方形。這個長方形的長和寬是多少？" % (who, a, n)
        return mcq(q, "長 %d 公分、寬 %d 公分" % (a * n, a), ["長 %d 公分、寬 %d 公分" % x for x in ((a * n, a * n), (a + n, a), (n, a), (a * n * 2, a))],
                   "排成一排，長是 %d × %d ＝ %d 公分，寬是 1 張的邊長 %d 公分。" % (a, n, a * n, a))
    return pick_unique(R, cut, 7, seen) + pick_unique(R, left, 6, seen) + pick_unique(R, tiles, 7, seen)


def main():
    seen = set()
    sets = [("認出正方形和長方形", s1(seen)), ("正方形和長方形的特徵", s2(seen)), ("邊長", s3(seen)),
            ("4 條邊一共多長", s4(seen)), ("剪一剪、拼一拼", s5(seen))]
    body = lesson(
        ["<b>長方形</b>：4 個角都是直角，相對的兩條邊一樣長。",
         "<b>正方形</b>：4 個角都是直角，<b>4 條邊都一樣長</b>。正方形是特別的長方形。",
         "判斷時邊和角都要看：4 邊一樣長但角不是直角的（菱形），不是正方形。"],
        [example("長方形的長 9 公分、寬 4 公分，4 條邊一共長幾公分？", ["長有 2 條，寬有 2 條。", "9 ＋ 9 ＋ 4 ＋ 4 ＝ 26。"], "26 公分"),
         example("用 28 公分的鐵絲圍成正方形，一邊長幾公分？", ["正方形 4 條邊一樣長。", "28 ÷ 4 ＝ 7。"], "7 公分")],
        [("4 條邊一樣長就是正方形", "還要 4 個角都是直角"),
         ("斜放的正方形不是正方形", "轉方向後邊和角都沒變"),
         ("長方形 4 條邊的總長 ＝ 長 ＋ 寬", "長和寬各有 2 條，要加兩次")])
    faq = [{"q": "正方形是長方形嗎？",
            "a": "是。長方形的特徵是 4 個直角、對邊等長；正方形全部符合，而且 4 邊都一樣長，所以正方形是特別的長方形。"},
           {"q": "三年級的正方形和長方形要學什麼？",
            "a": "108課綱 S-3-2：用「邊」和「角」的特徵來定義正方形和長方形，並能用三角板、尺檢查。"},
           {"q": "孩子把菱形說成正方形，怎麼辦？",
            "a": "請孩子用三角板的直角檢查 4 個角。菱形 4 邊一樣長，但角不是直角，所以不是正方形。"}]
    make_unit(R, "grade-3", "squares-and-rectangles", "S-3-2",
              "正方形和長方形：以邊與角的特徵來定義正方形和長方形。",
              "正方形和長方形：邊和角的特徵",
              "三年級數學 正方形和長方形 練習題｜邊和角的特徵・邊長 學習單（附解答）",
              "正方形和長方形",
              "國小三年級數學「正方形和長方形」免費學習單：用邊和角認出正方形和長方形、特徵判斷、邊長、4條邊的總長與剪拼問題。100題線上練習馬上對答案，附可列印解答。",
              "4 個直角＋4 邊等長 ＝ 正方形",
              "長方形：4 個直角、對邊等長。正方形是特別的長方形。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
