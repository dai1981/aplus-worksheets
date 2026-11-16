# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：三角形與四邊形的面積（108課綱 S-5-2）
  python3 tools/gen_tw_math_g5_area_of_triangles_and_quadrilaterals.py
平行四邊形＝底×高、三角形＝底×高÷2、梯形＝（上底＋下底）×高÷2（図つき・斜めの邊を罠に）、逆算、複合図形・應用。
誤答：斜めの邊を高として使う、三角形で ÷2 を忘れる、梯形で上底・下底を足し忘れる。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, RED, dnum

R = random.Random(51018)
NM = Names(R)
SC = 10


def shape_svg(kind, b, h, top=0, off=0, slant=None):
    """kind: para / tri / trap。b 底、h 高、top 上底、off 頂点のずれ、slant 斜めの邊の表示値"""
    ox, oy = (70 if slant else 30), 20
    if kind == "para":
        pts = [(off, 0), (off + b, 0), (b, h), (0, h)]
    elif kind == "tri":
        pts = [(off, 0), (b, h), (0, h)]
    else:
        pts = [(off, 0), (off + top, 0), (b, h), (0, h)]
    P = " ".join("%.1f,%.1f" % (ox + x * SC, oy + y * SC) for x, y in pts)
    s = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (P, FILL, GREEN)
    hx = ox + off * SC
    s += line(hx, oy, hx, oy + h * SC, RED, 2, " stroke-dasharray='5 4'")
    s += "<rect x='%.1f' y='%.1f' width='8' height='8' fill='none' stroke='%s' stroke-width='1.5'/>" % (hx, oy + h * SC - 8, RED)
    s += text(hx + 6, oy + h * SC / 2 + 5, "%s 公分" % h, 13, anchor="start", col=RED).replace("<text ", "<text stroke='#fff' stroke-width='4' paint-order='stroke' ", 1)
    s += text(ox + b * SC / 2, oy + h * SC + 18, "%s 公分" % b, 13)
    if kind == "trap":
        s += text(ox + (off + top / 2) * SC, oy - 6, "%s 公分" % top, 13)
    if slant:
        s += text(ox + off * SC / 2 - 6, oy + h * SC / 2, "%s 公分" % slant, 12, anchor="end")
    W = ox + max(x for x, y in pts) * SC + 70
    return fig(svg_wrap(int(W), int(oy + h * SC + 30), s, "圖形"))


def s1(seen):
    def mk():
        b, h = R.randint(6, 20), R.randint(4, 12)
        off = R.randint(2, 5)
        sl = round((off ** 2 + h ** 2) ** .5)
        if sl == h:
            return None
        q = "平行四邊形的面積是多少？（紅色虛線是高）" + shape_svg("para", b, h, off=off, slant=sl)
        A = b * h
        return mcq(q, "%d 平方公分" % A, ["%d 平方公分" % x for x in (b * sl, A // 2 if A % 2 == 0 else A + b, 2 * (b + sl)) if x != A],
                   "平行四邊形面積 ＝ 底 × 高 ＝ %d × %d ＝ %d（平方公分）。斜邊 %d 公分不是高。" % (b, h, A, sl))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        b, h = R.randint(4, 20), R.randint(3, 14)
        off = R.randint(0, b)
        q = "三角形的面積是多少？（紅色虛線是高）" + shape_svg("tri", b, h, off=off)
        A = b * h
        v = dnum(A / 2, 1)
        return mcq(q, "%s 平方公分" % v, ["%s 平方公分" % x for x in (num(A), dnum(A / 4, 2), num(b + h))], "三角形面積 ＝ 底 × 高 ÷ 2 ＝ %d × %d ÷ 2 ＝ %s（平方公分）。" % (b, h, v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        b, h = R.randint(8, 22), R.randint(4, 12)
        top = R.randint(3, b - 2)
        off = R.randint(1, b - top)
        q = "梯形的面積是多少？（紅色虛線是高）" + shape_svg("trap", b, h, top=top, off=off)
        A = (top + b) * h
        v = dnum(A / 2, 1)
        return mcq(q, "%s 平方公分" % v, ["%s 平方公分" % x for x in (num(A), dnum(b * h / 2, 1), num(top * b * h // 2) if (top * b * h) % 2 == 0 else dnum(top * b * h / 2, 1))],
                   "梯形面積 ＝（上底 ＋ 下底）× 高 ÷ 2 ＝（%d ＋ %d）× %d ÷ 2 ＝ %s（平方公分）。" % (top, b, h, v))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def back():
        kind = R.choice(["para", "tri", "trap"])
        h = R.randint(3, 12)
        if kind == "para":
            b = R.randint(4, 20)
            A = b * h
            q = "平行四邊形的面積是 %d 平方公分，底是 %d 公分，高是幾公分？" % (A, b)
            return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (A - b, A * b if A * b < 500 else A + b, h * 2)], "高 ＝ 面積 ÷ 底 ＝ %d ÷ %d ＝ %d（公分）。" % (A, b, h))
        if kind == "tri":
            b = R.randint(2, 15) * 2
            A = b * h // 2
            q = "三角形的面積是 %d 平方公分，底是 %d 公分，高是幾公分？" % (A, b)
            return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (A // b if A // b and A % b == 0 and A // b != h else h + 3, h * 2 if h * 2 != h else h + 1, A - b if A > b else h + 2)], "高 ＝ 面積 × 2 ÷ 底 ＝ %d × 2 ÷ %d ＝ %d（公分）。" % (A, b, h))
        t, b = R.randint(3, 10), R.randint(11, 20)
        if ((t + b) * h) % 2:
            return None
        A = (t + b) * h // 2
        q = "梯形的面積是 %d 平方公分，上底 %d 公分、下底 %d 公分，高是幾公分？" % (A, t, b)
        return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (A // (t + b) if A // (t + b) != h else h + 2, h * 2, A - t - b if A > t + b else h + 1)], "高 ＝ 面積 × 2 ÷（上底 ＋ 下底）＝ %d × 2 ÷ %d ＝ %d（公分）。" % (A, t + b, h))
    return pick_unique(R, back, 20, seen)


def s5(seen):
    def mk():
        kind = R.choice(["flag", "garden", "roof", "kite"])
        if kind == "flag":
            b, h = R.randint(20, 60), R.randint(15, 40)
            q = "一面三角形的旗子，底 %d 公分、高 %d 公分，面積是多少平方公分？" % (b, h)
            v = dnum(b * h / 2, 1)
            return mcq(q, v + " 平方公分", [num(b * h) + " 平方公分", dnum(b * h / 4, 2) + " 平方公分", num(b + h) + " 平方公分"], "%d × %d ÷ 2 ＝ %s（平方公分）。" % (b, h, v))
        if kind == "garden":
            t, b, h = R.randint(5, 15), R.randint(16, 30), R.randint(6, 20)
            q = "一塊梯形的花圃，上底 %d 公尺、下底 %d 公尺、高 %d 公尺，面積是多少平方公尺？" % (t, b, h)
            v = dnum((t + b) * h / 2, 1)
            return mcq(q, v + " 平方公尺", [num((t + b) * h) + " 平方公尺", num(t * b) + " 平方公尺", dnum(b * h / 2, 1) + " 平方公尺"], "（%d ＋ %d）× %d ÷ 2 ＝ %s（平方公尺）。" % (t, b, h, v))
        if kind == "roof":
            w, h1, h2 = R.randint(6, 14), R.randint(4, 8), R.randint(2, 5)
            q = "一個房子形狀的圖形，下面是長 %d 公分、寬 %d 公分的長方形，上面是底 %d 公分、高 %d 公分的三角形。面積是多少？" % (w, h1, w, h2)
            v = w * h1 + w * h2 / 2
            return mcq(q, dnum(v, 1) + " 平方公分", [dnum(w * h1 + w * h2, 1) + " 平方公分", dnum(w * (h1 + h2) / 2, 1) + " 平方公分", dnum(w * h1, 1) + " 平方公分"],
                       "長方形 %d × %d ＝ %d，三角形 %d × %d ÷ 2 ＝ %s，合起來 %s（平方公分）。" % (w, h1, w * h1, w, h2, dnum(w * h2 / 2, 1), dnum(v, 1)))
        b, h = R.randint(6, 20), R.randint(4, 15)
        q = "平行四邊形的停車格底 %d 公尺、高 %d 公尺，%d 格一共多少平方公尺？" % (b // 2 if b > 8 else b, h // 2 if h > 6 else h, 3)
        bb, hh = (b // 2 if b > 8 else b), (h // 2 if h > 6 else h)
        v = bb * hh * 3
        return mcq(q, "%d 平方公尺" % v, ["%d 平方公尺" % x for x in (bb * hh, bb * hh * 3 // 2 if (bb * hh * 3) % 2 == 0 else v + 3, (bb + hh) * 2 * 3)], "一格 %d × %d ＝ %d，3 格 %d × 3 ＝ %d（平方公尺）。" % (bb, hh, bb * hh, bb * hh, v))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("平行四邊形的面積", s1(seen)), ("三角形的面積", s2(seen)), ("梯形的面積", s3(seen)), ("已知面積求高", s4(seen)), ("應用問題", s5(seen))]
    demo = shape_svg("tri", 10, 6, off=3)
    body = lesson(
        ["<b>平行四邊形</b>剪下一個三角形移到另一邊，變成長方形：面積 ＝ <b>底 × 高</b>。",
         "兩個一樣的<b>三角形</b>可以拼成平行四邊形：面積 ＝ <b>底 × 高 ÷ 2</b>。",
         "兩個一樣的<b>梯形</b>可以拼成平行四邊形：面積 ＝ <b>（上底 ＋ 下底）× 高 ÷ 2</b>。",
         "「高」是和底垂直的那條線，不是斜斜的邊。"],
        [example("三角形面積是多少？" + demo, ["底 10 公分、高 6 公分。", "10 × 6 ÷ 2 ＝ 30。"], "30 平方公分"),
         example("上底 5、下底 9、高 4 公分的梯形面積？", ["（5 ＋ 9）× 4 ÷ 2 ＝ 28。"], "28 平方公分")],
        [("用斜邊當高", "高要和底垂直（圖上有直角記號的那條）"),
         ("三角形忘了 ÷ 2", "三角形是平行四邊形的一半"),
         ("梯形只用下底 × 高 ÷ 2", "上底和下底要先加起來")])
    faq = [{"q": "三角形、平行四邊形、梯形的面積公式是什麼？",
            "a": "平行四邊形 ＝ 底 × 高；三角形 ＝ 底 × 高 ÷ 2；梯形 ＝（上底 ＋ 下底）× 高 ÷ 2。"},
           {"q": "為什麼三角形面積要除以 2？",
            "a": "兩個一模一樣的三角形可以拼成一個平行四邊形，所以三角形面積是平行四邊形的一半。"},
           {"q": "五年級的面積要學什麼？",
            "a": "108課綱 S-5-2：利用切割重組，建立三角形、平行四邊形、梯形的面積公式，並能應用。"}]
    make_unit(R, "grade-5", "area-of-triangles-and-quadrilaterals", "S-5-2",
              "三角形與四邊形的面積：操作活動與推理。利用切割重組，建立面積公式，並能應用。",
              "三角形、平行四邊形、梯形的面積",
              "五年級數學 面積公式 練習題｜三角形・平行四邊形・梯形面積 學習單（附解答）",
              "三角形和四邊形的面積",
              "國小五年級數學「三角形與四邊形的面積」免費學習單：平行四邊形、三角形、梯形的面積公式，已知面積求高與應用題。100題線上練習馬上對答案，附可列印解答。",
              "三角形 ＝ 底 × 高 ÷ 2",
              "平行四邊形 ＝ 底 × 高；梯形 ＝（上底 ＋ 下底）× 高 ÷ 2。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
