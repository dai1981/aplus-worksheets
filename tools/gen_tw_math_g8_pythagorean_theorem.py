# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：畢氏定理（108課綱 S-8-6）
  python3 tools/gen_tw_math_g8_pythagorean_theorem.py
直角三角形の斜邊 c²＝a²＋b²、斜邊・股を求める（整數・根式）、直角三角形かどうかの判定（逆）、生活の應用（梯子・對角線・最短距離）、數學史（勾股弦・商高定理）。
誤答：斜邊を求めるのに引き算する、股を求めるのに足す、a＋b＝c とする、最長邊以外を斜邊とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK, RED
from tw_g8 import tidy_sets, rt, simp

R = random.Random(81007)
NM = Names(R)
TRI = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29), (9, 40, 41), (15, 20, 25), (10, 24, 26)]


def tri_svg(a, b, la, lb, lc):
    sc = 150 / max(a, b)
    W, H = int(b * sc) + 90, int(a * sc) + 50
    ox, oy = 40, 20 + a * sc
    A, B, C = (ox, oy - a * sc), (ox, oy), (ox + b * sc, oy)
    s = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (A + B + C + (FILL, GREEN)),
         "<path d='M%.1f %.1f h12 v-12' fill='none' stroke='%s' stroke-width='1.4'/>" % (B[0], B[1] - 0, INK)]
    s[1] = "<path d='M%.1f %.1f v-12 h12' fill='none' stroke='%s' stroke-width='1.4'/>" % (B[0], B[1], INK)
    s.append(text(ox - 8, (A[1] + B[1]) / 2 + 4, la, 13, anchor="end", col=RED if la == "x" else INK))
    s.append(text((B[0] + C[0]) / 2, oy + 18, lb, 13, col=RED if lb == "x" else INK))
    s.append(text((A[0] + C[0]) / 2 + 10, (A[1] + C[1]) / 2 - 6, lc, 13, anchor="start", col=RED if lc == "x" else INK))
    return fig(svg_wrap(W, H, "".join(s), "直角三角形"))


def s1(seen):
    def mk():
        a, b, c = R.choice(TRI)
        if R.random() < .5:
            a, b = b, a
        g = tri_svg(a, b, str(a), str(b), "x")
        return mcq("求直角三角形的斜邊 x。" + g, str(c), [str(a + b), str(abs(b - a)) if a != b else str(c + 1), "√%d" % abs(b * b - a * a) if b != a else str(c + 2), str(c + 1)], "x<sup>2</sup> ＝ %d<sup>2</sup> ＋ %d<sup>2</sup> ＝ %d，x ＝ %d。" % (a, b, c * c, c))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b, c = R.choice(TRI)
        if R.random() < .5:
            a, b = b, a
        if R.random() < .5:
            g = tri_svg(a, b, "x", str(b), str(c))
            ans, other = a, b
        else:
            g = tri_svg(a, b, str(a), "x", str(c))
            ans, other = b, a
        k, m = simp(c * c + other * other)
        return mcq("求直角三角形的邊長 x。" + g, str(ans), [str(c - other), rt(k, m), str(ans + 1)], "x 是股：x<sup>2</sup> ＝ %d<sup>2</sup> － %d<sup>2</sup> ＝ %d，x ＝ %d。" % (c, other, ans * ans, ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a > b:
            a, b = b, a
        k = R.choice(["hyp", "leg"])
        if k == "hyp":
            s = a * a + b * b
            kk, m = simp(s)
            if m == 1:
                return None
            q = "直角三角形的兩股是 %d 和 %d，斜邊是多少？" % (a, b)
            return mcq(q, rt(kk, m), [str(a + b), "√%d" % (b * b - a * a) if b != a else rt(kk + 1, m), rt(kk, m + 1)], "斜邊<sup>2</sup> ＝ %d ＋ %d ＝ %d，斜邊 ＝ √%d%s。" % (a * a, b * b, s, s, "" if kk == 1 else " ＝ " + rt(kk, m)))
        c = b + R.randint(1, 4)
        s = c * c - a * a
        kk, m = simp(s)
        if m == 1:
            return None
        q = "直角三角形的斜邊是 %d，一股是 %d，另一股是多少？" % (c, a)
        return mcq(q, rt(kk, m), [rt(*simp(c * c + a * a)), str(c - a), rt(kk + 1, m)], "另一股<sup>2</sup> ＝ %d － %d ＝ %d，另一股 ＝ √%d%s。" % (c * c, a * a, s, s, "" if kk == 1 else " ＝ " + rt(kk, m)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        if R.random() < .5:
            a, b, c = R.choice(TRI)
            ok = True
        else:
            a, b = R.randint(2, 15), R.randint(2, 15)
            c = int((a * a + b * b) ** .5) + R.choice([0, 1])
            ok = a * a + b * b == c * c
            if ok or c <= max(a, b):
                return None
        sides = [a, b, c]
        R.shuffle(sides)
        q = "三邊長為 %s 的三角形是直角三角形嗎？" % "、".join(map(str, sides))
        big = max(sides)
        oth = [x for x in sides if x != big] if len(set(sides)) == 3 else sorted(sides)[:2]
        return mcq(q, "是" if ok else "不是", ["不是" if ok else "是", "無法判斷", "只有等腰才能判斷"],
                   "最長邊 %d：%d<sup>2</sup> ＋ %d<sup>2</sup> ＝ %d，%d<sup>2</sup> ＝ %d，%s。" % (big, oth[0], oth[1], oth[0] ** 2 + oth[1] ** 2, big, big * big, "相等，是直角三角形" if ok else "不相等，不是直角三角形"))

    def hist():
        F_ = [("畢氏定理在中國古代又叫做什麼？", "勾股弦定理（商高定理）", ["九九乘法", "割圓術", "祖沖之定理"], "《周髀算經》記載商高「勾三股四弦五」。"),
              ("「勾三股四弦五」是指什麼？", "直角三角形兩股 3、4 時斜邊是 5", ["三角形周長是 12", "正方形邊長 3、4、5", "3、4、5 是質數"], "3<sup>2</sup> ＋ 4<sup>2</sup> ＝ 5<sup>2</sup>。"),
              ("畢氏定理適用於哪一種三角形？", "直角三角形", ["所有三角形", "正三角形", "鈍角三角形"], "只有直角三角形才有 a<sup>2</sup> ＋ b<sup>2</sup> ＝ c<sup>2</sup>。"),
              ("直角三角形中最長的邊是哪一邊？", "斜邊（直角的對邊）", ["任意一股", "最短的股", "一樣長"], "斜邊對著直角，是最長的邊。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, mk, 16, seen) + pick_unique(R, hist, 4, seen)


def s5(seen):
    def ladder():
        a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
        if R.random() < .5:
            a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13)])
            q = "一把 %d 公尺長的%s靠在牆上，梯腳離牆 %d 公尺。梯子頂端離地多高？" % (c, "梯子" if c <= 5 else "消防雲梯", a)
            return mcq(q, "%d 公尺" % b, ["%d 公尺" % x for x in (c - a, a + c, b + 1)], "高<sup>2</sup> ＝ %d<sup>2</sup> － %d<sup>2</sup> ＝ %d，高 ＝ %d 公尺。" % (c, a, b * b, b))
        q = "一塊長方形看板寬 %d 公寸、高 %d 公寸，對角線是幾公寸？" % (b * 2 if b * 2 < 70 else b, a * 2 if b * 2 < 70 else a)
        w, h = (b * 2, a * 2) if b * 2 < 70 else (b, a)
        d = c * (2 if b * 2 < 70 else 1)
        return mcq(q, "%d 公寸" % d, ["%d 公寸" % x for x in (w + h, w * h // 10 if w * h // 10 != d else d + 3, d + 2)], "對角線<sup>2</sup> ＝ %d<sup>2</sup> ＋ %d<sup>2</sup>，對角線 ＝ %d 公寸。" % (w, h, d))

    def walk():
        a, b, c = R.choice(TRI[:6])
        q = "%s從家往東走 %d 公尺，再往北走 %d 公尺到學校。家到學校的直線距離是多少公尺？" % (NM.next(), a * 10, b * 10)
        return mcq(q, "%d 公尺" % (c * 10), ["%d 公尺" % x for x in ((a + b) * 10, (b - a) * 10 if b > a else (a - b) * 10 + 5, c * 10 + 10)], "直線距離<sup>2</sup> ＝ %d<sup>2</sup> ＋ %d<sup>2</sup>，距離 ＝ %d 公尺。" % (a * 10, b * 10, c * 10))

    def rect():
        a, b = R.randint(2, 9), R.randint(2, 9)
        s = a * a + b * b
        k, m = simp(s)
        q = "長方形的長 %d 公分、寬 %d 公分，對角線長多少公分？" % (max(a, b), min(a, b))
        return mcq(q, "%s 公分" % rt(k, m), ["%s 公分" % x for x in (str(a + b), "√%d" % (a + b), rt(k + 1, m) if m > 1 else str(k + 1))], "對角線<sup>2</sup> ＝ %d ＋ %d ＝ %d，對角線 ＝ %s。" % (a * a, b * b, s, rt(k, m)))
    return pick_unique(R, ladder, 7, seen) + pick_unique(R, walk, 6, seen) + pick_unique(R, rect, 7, seen)


def main():
    seen = set()
    sets = [("求斜邊", s1(seen)), ("求股", s2(seen)), ("答案是根式", s3(seen)),
            ("判斷直角三角形", s4(seen)), ("生活應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["直角三角形中，兩股為 a、b，斜邊（直角的對邊，最長）為 c：<b>a<sup>2</sup> ＋ b<sup>2</sup> ＝ c<sup>2</sup></b>。",
         "求斜邊：兩股平方<b>相加</b>再開方；求股：斜邊平方<b>減</b>另一股平方再開方。",
         "反過來：三邊滿足 a<sup>2</sup> ＋ b<sup>2</sup> ＝ c<sup>2</sup>（c 最長），就是直角三角形。",
         "常見整數組：3、4、5；5、12、13；8、15、17；7、24、25。"],
        [example("兩股 6、8，斜邊？", ["36 ＋ 64 ＝ 100。"], "10"),
         example("斜邊 13、一股 5，另一股？", ["169 － 25 ＝ 144。"], "12")],
        [("兩股 3、4，斜邊 7", "要平方再相加：√25 ＝ 5"),
         ("求股時把兩數平方相加", "求股要相減"),
         ("把不是最長的邊當斜邊", "斜邊一定是最長邊")])
    faq = [{"q": "畢氏定理是什麼？",
            "a": "直角三角形中，兩股的平方和等於斜邊的平方：a² ＋ b² ＝ c²。中國古代稱為勾股弦定理或商高定理。"},
           {"q": "怎麼判斷三角形是不是直角三角形？",
            "a": "把最長邊平方，和另外兩邊的平方和比較，相等就是直角三角形。"},
           {"q": "八年級的畢氏定理要學什麼？",
            "a": "108課綱 S-8-6：畢氏定理的意義及其數學史、在生活上的應用，以及三邊長滿足畢氏定理的三角形必定是直角三角形。"}]
    make_unit(R, "grade-8", "pythagorean-theorem", "S-8-6",
              "畢氏定理：畢氏定理（勾股弦定理、商高定理）的意義及其數學史；畢氏定理在生活上的應用；三邊長滿足畢氏定理的三角形必定是直角三角形。",
              "畢氏定理（勾股弦定理）",
              "八年級數學 畢氏定理 練習題｜斜邊・股・判斷直角三角形・梯子 學習單（附解答）",
              "畢氏定理",
              "國中八年級數學「畢氏定理」免費學習單：求斜邊和股、答案是根式的情形、判斷直角三角形、勾股弦的數學史與梯子、對角線、距離等生活應用。100題線上練習馬上對答案，附可列印解答。",
              "a² ＋ b² ＝ c²（c 是斜邊）",
              "求斜邊用加，求股用減。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
