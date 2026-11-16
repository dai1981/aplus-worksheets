# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：數量模式與推理（二維數字圖、奇數與偶數）（108課綱 R-4-4）
  python3 tools/gen_tw_math_g4_patterns_odd_even.py
百數表・日曆の上下左右・斜め、九九乘法表の規律、奇數・偶數の判別、和・差・積の奇偶、正方形に並べた點の規律。
誤答：下は ＋1 と思う（＋10・＋7）、奇數＋奇數＝奇數、奇數×偶數＝奇數。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK, RED

R = random.Random(41023)
NM = Names(R)


def grid_svg(start, cols, rows, hide, show_cols=None):
    C = 40
    s = []
    for r in range(rows):
        for c in range(cols):
            v = start + r * cols + c
            x, y = 10 + c * C, 10 + r * C
            hid = v == hide
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y, C, C, "#fde9e7" if hid else "#fff", GREEN))
            s.append(text(x + C / 2, y + C / 2 + 6, "?" if hid else str(v), 15, col=RED if hid else INK))
    return fig(svg_wrap(cols * C + 20, rows * C + 20, "".join(s), "數字表"))


def s1(seen):
    def mk():
        cols = R.choice([10, 10, 7])
        rows = 3
        start = R.randint(1, 60) if cols == 10 else 1 + 7 * R.randint(0, 2)
        if cols == 10:
            start = start // 10 * 10 + 1
        r0, c0 = 1, R.randint(1, cols - 2)
        center = start + r0 * cols + c0
        d = R.choice([("下面", cols), ("上面", -cols), ("右下", cols + 1), ("左下", cols - 1)])
        hide = center + d[1]
        q = ("這是%s的一部分。中間的 %d %s的數是多少？" % ("百數表" if cols == 10 else "月曆（每排 7 天）", center, d[0])) + grid_svg(start, cols, rows, hide)
        return mcq(q, str(hide), [str(center + x) for x in (1, -1, cols + 2, cols * 2, 10 if cols == 7 else 7) if center + x != hide],
                   "每排有 %d 個數，%s是 %s%d：%d %s %d ＝ %d。" % (cols, d[0], "＋" if d[1] > 0 else "－", abs(d[1]), center, "＋" if d[1] > 0 else "－", abs(d[1]), hide))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        kind = R.choice(["row", "col", "cell"])
        a = R.randint(2, 9)
        if kind == "row":
            q = "九九乘法表中，%d 的那一排（%d × 1、%d × 2、%d × 3……）每次增加多少？" % (a, a, a, a)
            return mcq(q, "每次加 %d" % a, ["每次加 %d" % x for x in (1, a + 1, 2 * a, 10) if x != a][:3], "%d × 1 ＝ %d，%d × 2 ＝ %d，每次多一個 %d。" % (a, a, a, 2 * a, a))
        if kind == "col":
            b = R.randint(2, 9)
            q = "九九乘法表中，%d × %d 往下一格是 %d × %d，增加多少？" % (a, b, a + 1, b) if a < 9 else None
            if not q:
                return None
            return mcq(q, "增加 %d" % b, ["增加 %d" % x for x in (a, 1, a + b, a * b) if x != b][:3], "多乘一次 %d：%d × %d － %d × %d ＝ %d。" % (b, a + 1, b, a, b, b))
        b = R.randint(2, 9)
        q = "九九乘法表中，%d × %d 和 %d × %d 的答案有什麼關係？" % (a, b, b, a)
        if a == b:
            return None
        return mcq(q, "一樣大", ["%d × %d 比較大" % (max(a, b), min(a, b)), "%d × %d 比較大" % (min(a, b), max(a, b)), "不能比較"], "乘法交換律：%d × %d ＝ %d × %d ＝ %d，乘法表左上到右下的線兩邊對稱。" % (a, b, b, a, a * b))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def which():
        n = R.randint(10, 9999)
        odd = n % 2 == 1
        q = "%d 是奇數還是偶數？" % n
        return mcq(q, "奇數" if odd else "偶數", ["偶數" if odd else "奇數", "都不是", "要看十位"], "看個位：%d 是%s，所以 %d 是%s。（個位是 1、3、5、7、9 是奇數；0、2、4、6、8 是偶數）" % (n % 10, "奇數" if odd else "偶數", n, "奇數" if odd else "偶數"))

    def add():
        a, b = R.randint(10, 999), R.randint(10, 999)
        op = R.choice(["＋", "－"])
        if op == "－" and a < b:
            a, b = b, a
        v = a + b if op == "＋" else a - b
        q = "不用算出答案，%d %s %d 的結果是奇數還是偶數？" % (a, op, b)
        pa, pb = "奇" if a % 2 else "偶", "奇" if b % 2 else "偶"
        ans = "奇數" if v % 2 else "偶數"
        return mcq(q, ans, ["偶數" if v % 2 else "奇數", "不一定", "要算出來才知道"], "%s數 %s %s數 ＝ %s。" % (pa, op, pb, ans))
    return pick_unique(R, which, 8, seen) + pick_unique(R, add, 12, seen)


def s4(seen):
    def mul():
        a, b = R.randint(3, 99), R.randint(3, 99)
        v = a * b
        q = "不用算出答案，%d × %d 的結果是奇數還是偶數？" % (a, b)
        ans = "奇數" if v % 2 else "偶數"
        return mcq(q, ans, ["偶數" if v % 2 else "奇數", "不一定", "要算出來才知道"], "只要乘的兩個數中有一個是偶數，積就是偶數；兩個都是奇數，積才是奇數：%s。" % ans)

    def rule():
        F = [("奇數 ＋ 奇數 ＝ ？", "偶數", ["奇數", "不一定", "0"], "例如 3 ＋ 5 ＝ 8，是偶數。"),
             ("奇數 ＋ 偶數 ＝ ？", "奇數", ["偶數", "不一定", "0"], "例如 3 ＋ 4 ＝ 7，是奇數。"),
             ("偶數 ＋ 偶數 ＝ ？", "偶數", ["奇數", "不一定", "0"], "例如 2 ＋ 6 ＝ 8，是偶數。"),
             ("奇數 × 奇數 ＝ ？", "奇數", ["偶數", "不一定", "0"], "例如 3 × 5 ＝ 15，是奇數。"),
             ("奇數 × 偶數 ＝ ？", "偶數", ["奇數", "不一定", "0"], "例如 3 × 4 ＝ 12，是偶數。"),
             ("偶數 － 奇數 ＝ ？", "奇數", ["偶數", "不一定", "0"], "例如 10 － 3 ＝ 7，是奇數。"),
             ("奇數 － 奇數 ＝ ？", "偶數", ["奇數", "不一定", "1"], "例如 9 － 5 ＝ 4，是偶數。"),
             ("1 到 20 之間有幾個偶數？", "10 個", ["9 個", "11 個", "20 個"], "2、4、6……20，共 10 個。"),
             ("三個奇數加起來是奇數還是偶數？", "奇數", ["偶數", "不一定", "要看是哪三個"], "奇 ＋ 奇 ＝ 偶，偶 ＋ 奇 ＝ 奇。"),
             ("一排有 7 個人，要兩人一組，會不會剛好分完？", "不會，多 1 人", ["會，剛好分完", "不會，多 2 人", "不會，少 2 人"], "7 是奇數，兩個兩個分會多 1 個。")]
        return mcq(*R.choice(F))
    return pick_unique(R, mul, 10, seen) + pick_unique(R, rule, 10, seen)


def dots(n):
    C = 14
    s = "".join("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (10 + c * C, 10 + r * C, GREEN) for r in range(n) for c in range(n))
    return s, n * C + 6


def s5(seen):
    def sq():
        n = R.randint(5, 15)
        s, w = "", 10
        for k in (1, 2, 3, 4):
            b, ww = dots(k)
            s += "<g transform='translate(%d 0)'>%s</g>" % (w, b) + text(w + ww / 2, 80, "第 %d 個" % k, 11)
            w += ww + 18
        q = "點排成正方形，照這樣排下去，第 %d 個有幾個點？" % n + fig(svg_wrap(int(w), 88, s, "排成正方形的點"))
        return mcq(q, "%d 個" % (n * n), ["%d 個" % x for x in (4 * n, 2 * n, n * n + n, (n - 1) * (n - 1))], "第 %d 個是 %d 排、每排 %d 個：%d × %d ＝ %d。" % (n, n, n, n, n, n * n))

    def oddsum():
        n = R.randint(3, 12)
        terms = [2 * i + 1 for i in range(n)]
        q = "%s ＝ ？（找規律：1 ＝ 1，1 ＋ 3 ＝ 4，1 ＋ 3 ＋ 5 ＝ 9……）" % " ＋ ".join(str(t) for t in terms)
        return mcq(q, str(n * n), [str(x) for x in (n * (n + 1), 2 * n * n, n * n - 1, (n + 1) * (n + 1))], "從 1 開始連續 %d 個奇數相加，等於 %d × %d ＝ %d。" % (n, n, n, n * n))

    def nth_odd():
        n = R.randint(8, 50)
        ask = R.choice(["奇數", "偶數"])
        v = 2 * n - 1 if ask == "奇數" else 2 * n
        q = "從小到大，第 %d 個%s是多少？（%s）" % (n, ask, "1、3、5、7……" if ask == "奇數" else "2、4、6、8……")
        return mcq(q, str(v), [str(x) for x in (v + 2, v - 2, n, 2 * n + 1 if ask == "奇數" else 2 * n - 1)], "第 n 個%s是 %s：%s。" % (ask, "2 × n － 1" if ask == "奇數" else "2 × n", v))
    return pick_unique(R, sq, 6, seen) + pick_unique(R, oddsum, 7, seen) + pick_unique(R, nth_odd, 7, seen)


def main():
    seen = set()
    sets = [("百數表和月曆", s1(seen)), ("九九乘法表的規律", s2(seen)), ("奇數和偶數", s3(seen)),
            ("奇偶的乘法規律", s4(seen)), ("圖形和數的規律", s5(seen))]
    body = lesson(
        ["<b>二維數字圖</b>：百數表一排 10 個，往下一格 ＋10；月曆一排 7 天，往下一格 ＋7。",
         "<b>偶數</b>：個位是 0、2、4、6、8；<b>奇數</b>：個位是 1、3、5、7、9。",
         "奇 ＋ 奇 ＝ 偶，奇 ＋ 偶 ＝ 奇，偶 ＋ 偶 ＝ 偶；乘法只要有一個偶數，積就是偶數。"],
        [example("月曆上 12 日下面一格是幾日？", ["一排 7 天，往下 ＋7。", "12 ＋ 7 ＝ 19。"], "19 日"),
         example("357 ＋ 486 是奇數還是偶數？", ["357 是奇數，486 是偶數。", "奇 ＋ 偶 ＝ 奇。"], "奇數")],
        [("百數表往下一格 ＋1", "往右才 ＋1，往下是 ＋10"),
         ("奇數 ＋ 奇數 ＝ 奇數", "3 ＋ 5 ＝ 8，是偶數"),
         ("奇數 × 偶數 ＝ 奇數", "3 × 4 ＝ 12，只要有偶數，積就是偶數")])
    faq = [{"q": "怎麼判斷奇數和偶數？",
            "a": "只要看個位：0、2、4、6、8 是偶數，1、3、5、7、9 是奇數。偶數可以兩個兩個剛好分完。"},
           {"q": "四年級的數量模式要學什麼？",
            "a": "108課綱 R-4-4：觀察和推理二維的變化模式（如百數表、月曆、乘法表），以及奇數與偶數在加、減、乘時的規律。"},
           {"q": "為什麼奇數加奇數是偶數？",
            "a": "奇數兩個兩個分會多 1 個，兩個奇數各多出的 1 個合起來又湊成一對，所以剛好分完，是偶數。"}]
    make_unit(R, "grade-4", "patterns-odd-and-even", "R-4-4",
              "數量模式與推理（II）：以操作活動為主。二維變化模式之觀察與推理，如二維數字圖之推理。奇數與偶數，及其加、減、乘模式。",
              "數量模式與推理：二維數字圖、奇數與偶數",
              "四年級數學 奇數偶數 練習題｜百數表・月曆・乘法表規律・奇偶規律 學習單（附解答）",
              "奇數偶數與規律",
              "國小四年級數學「數量模式與推理」免費學習單：百數表和月曆的規律、九九乘法表的規律、奇數和偶數、奇偶的加減乘規律和圖形的規律。100題線上練習馬上對答案，附可列印解答。",
              "奇 ＋ 奇 ＝ 偶，奇 × 偶 ＝ 偶",
              "百數表往下 ＋10，月曆往下 ＋7。",
              body, faq, sets, 23)


if __name__ == "__main__":
    main()
