# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：特殊直角三角形的邊長比（108課綱 S-9-4）
  python3 tools/gen_tw_math_g9_special_right_triangles.py
45°-45°-90°（1：1：√2）、30°-60°-90°（1：√3：2）、斜邊・股から他の邊、整數が根號になる場合（有理化）、正方形の對角線・正三角形の高などの複合、坡道・梯子の應用。
誤答：30° の對邊と 60° の對邊を取り違える、斜邊を √3 倍にする、√2 で割る代わりに掛ける。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fig, svg_wrap, text, line, INK, RED, BLUE
from tw_g7 import tidy_sets

R = random.Random(81105)


def rd(k, m):
    """k√m（m＝1 なら整数）"""
    if m == 1:
        return str(k)
    return "√%d" % m if k == 1 else "%d√%d" % (k, m)


def tri_svg(kind, lab):
    """kind 45/30：直角は左下。lab: {'a':底邊,'b':高,'c':斜邊}"""
    if kind == 45:
        B, C, A = (30, 150), (170, 150), (30, 10)
    else:
        B, C, A = (30, 150), (200, 150), (30, 52)
    s = [line(B[0], B[1], C[0], C[1], INK, 2), line(B[0], B[1], A[0], A[1], INK, 2), line(A[0], A[1], C[0], C[1], INK, 2),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (B[0] + 12, B[1], B[0] + 12, B[1] - 12, B[0], B[1] - 12, INK)]
    angC = "45°" if kind == 45 else "30°"
    angA = "45°" if kind == 45 else "60°"
    s.append(text(C[0] - 36, C[1] - 6, angC, 12))
    s.append(text(A[0] + 14, A[1] + 26, angA, 12))
    col = lambda t: RED if t == "x" else BLUE
    if lab.get("a"):
        s.append(text((B[0] + C[0]) / 2, B[1] + 18, lab["a"], 14, col=col(lab["a"])))
    if lab.get("b"):
        s.append(text(B[0] - 8, (A[1] + B[1]) / 2 + 5, lab["b"], 14, "end", col=col(lab["b"])))
    if lab.get("c"):
        s.append(text((A[0] + C[0]) / 2 + 14, (A[1] + C[1]) / 2 - 6, lab["c"], 14, "start", col=col(lab["c"])))
    return fig(svg_wrap(230, 175, "".join(s), "%d°直角三角形" % kind))


def s1(seen):
    def mk():
        k = R.randint(2, 20)
        t = R.choice(["leg", "hyp", "hyp_int"])
        if t == "leg":
            q = "求斜邊 x。" + tri_svg(45, {"a": str(k), "b": str(k), "c": "x"})
            return mcq(q, rd(k, 2), [rd(k, 3), rd(2 * k, 1), rd(k * 2, 2)], "45°-45°-90° 的邊長比 1：1：√2，斜邊 ＝ %d × √2 ＝ %s。" % (k, rd(k, 2)))
        if t == "hyp":
            q = "求股長 x。" + tri_svg(45, {"a": "x", "c": rd(k, 2)})
            return mcq(q, str(k), [rd(k, 2), rd(2 * k, 1), "%d" % (k * 2)], "1：√2 ＝ x：%s，x ＝ %d。" % (rd(k, 2), k))
        h = 2 * k
        q = "等腰直角三角形的斜邊長 %d，股長是多少？" % h
        return mcq(q, rd(k, 2), [str(k), rd(h, 2), rd(k, 3)], "股 ＝ %d ÷ √2 ＝ <span class='fr'><span class='fn'>%d√2</span><span class='fd'>2</span></span> ＝ %s。" % (h, h, rd(k, 2)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        k = R.randint(2, 20)
        t = R.choice(["short_hyp", "short_long"])
        if t == "short_hyp":
            q = "求斜邊 x。" + tri_svg(30, {"b": str(k), "c": "x"})
            return mcq(q, str(2 * k), [rd(k, 3), rd(k, 2), str(3 * k)], "30°-60°-90° 的邊長比 1：√3：2，30° 的對邊 %d 是最短邊，斜邊 ＝ 2 × %d ＝ %d。" % (k, k, 2 * k))
        q = "求 x。" + tri_svg(30, {"b": str(k), "a": "x"})
        return mcq(q, rd(k, 3), [str(2 * k), rd(k, 2), rd(2 * k, 3)], "30° 的對邊是 %d，60° 的對邊 ＝ %d × √3 ＝ %s。" % (k, k, rd(k, 3)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.randint(2, 15)
        t = R.choice(["hyp", "long", "long_int"])
        if t == "hyp":
            q = "30°-60°-90° 的直角三角形，斜邊長 %d，60° 角的對邊長是多少？" % (2 * k)
            return mcq(q, rd(k, 3), [str(k), rd(2 * k, 3), rd(k, 2)], "最短邊 ＝ %d ÷ 2 ＝ %d，60° 的對邊 ＝ %s。" % (2 * k, k, rd(k, 3)))
        if t == "long":
            q = "30°-60°-90° 的直角三角形，60° 角的對邊長 %s，斜邊長是多少？" % rd(k, 3)
            return mcq(q, str(2 * k), [str(k), rd(2 * k, 3), str(3 * k)], "最短邊 ＝ %d，斜邊 ＝ 2 × %d ＝ %d。" % (k, k, 2 * k))
        m = 3 * k
        q = "30°-60°-90° 的直角三角形，60° 角的對邊長 %d，最短邊長是多少？" % m
        return mcq(q, rd(k, 3), [str(k), rd(m, 3), str(m // 3 * 2)], "最短邊 ＝ %d ÷ √3 ＝ <span class='fr'><span class='fn'>%d√3</span><span class='fd'>3</span></span> ＝ %s。" % (m, m, rd(k, 3)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def sq():
        k = R.randint(2, 20)
        q = "邊長 %d 的正方形，對角線長是多少？" % k
        return mcq(q, rd(k, 2), [str(2 * k), rd(k, 3), rd(2 * k, 2)], "對角線把正方形分成兩個 45°-45°-90° 的三角形：%d × √2 ＝ %s。" % (k, rd(k, 2)))

    def eq():
        k = R.randint(1, 12)
        a = 2 * k
        q = "邊長 %d 的正三角形，高是多少？" % a
        return mcq(q, rd(k, 3), [str(k), rd(a, 3), rd(k, 2)], "高把正三角形分成兩個 30°-60°-90° 的三角形，最短邊 %d，高 ＝ %s。" % (k, rd(k, 3)))

    def rect():
        k = R.randint(2, 12)
        q = "長方形的對角線長 %d，對角線和長邊的夾角是 30°，短邊長是多少？" % (2 * k)
        return mcq(q, str(k), [rd(k, 3), str(2 * k), rd(k, 2)], "短邊是 30° 的對邊，等於斜邊（對角線）的一半：%d。" % k)
    return pick_unique(R, sq, 7, seen) + pick_unique(R, eq, 7, seen) + pick_unique(R, rect, 6, seen)


def s5(seen):
    def ladder():
        L = R.choice([2, 3, 4, 5, 6])
        ang = R.choice([60, 30])
        q = "一把長 %d 公尺的梯子靠在牆上，梯子和地面的夾角是 %d°。梯腳離牆多少公尺？" % (L * 2, ang)
        if ang == 60:
            return mcq(q, "%d 公尺" % L, ["%s 公尺" % rd(L, 3), "%d 公尺" % (2 * L), "%s 公尺" % rd(L, 2)], "梯子是斜邊，梯腳到牆是 60° 的鄰邊（30° 的對邊），等於斜邊的一半：%d 公尺。" % L)
        return mcq(q, "%s 公尺" % rd(L, 3), ["%d 公尺" % L, "%d 公尺" % (2 * L), "%s 公尺" % rd(L, 2)], "梯腳到牆是 30° 的鄰邊（60° 的對邊）：%d × √3 ＝ %s 公尺。" % (L, rd(L, 3)))

    def ramp():
        h = R.choice([1, 2, 3, 4, 5])
        q = "一條坡道和地面的夾角是 30°，坡道頂端高 %d 公尺，坡道長多少公尺？" % h
        return mcq(q, "%d 公尺" % (2 * h), ["%s 公尺" % rd(h, 3), "%d 公尺" % h, "%s 公尺" % rd(h, 2)], "高是 30° 的對邊，坡道是斜邊：2 × %d ＝ %d 公尺。" % (h, 2 * h))

    def kite():
        L = R.choice([10, 20, 30, 40, 50])
        q = "風箏線放出 %d 公尺，拉直後和地面成 45°，風箏離地面約多少公尺？（√2 ≈ 1.414，手的高度不計）" % L
        v = L / 1.414
        return mcq(q, "%.1f 公尺" % v, ["%.1f 公尺" % x for x in (L * 1.414, L / 2, L / 1.732)], "斜邊 %d，高 ＝ %d ÷ √2 ≈ %.1f 公尺。" % (L, L, v))
    return pick_unique(R, ladder, 8, seen) + pick_unique(R, ramp, 5, seen) + pick_unique(R, kite, 5, seen) + pick_unique(R, ladder, 2, seen)


def main():
    seen = set()
    sets = [("45°-45°-90°", s1(seen)), ("30°-60°-90°：由最短邊求", s2(seen)), ("30°-60°-90°：由斜邊或長股求", s3(seen)),
            ("正方形、正三角形和長方形", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["直角三角形的一個銳角決定了三邊的比，和三角形的大小無關。",
         "<b>45°-45°-90°</b>：兩股：斜邊 ＝ <b>1：1：√2</b>。" + tri_svg(45, {"a": "1", "b": "1", "c": "√2"}),
         "<b>30°-60°-90°</b>：30° 的對邊：60° 的對邊：斜邊 ＝ <b>1：√3：2</b>。最短邊是斜邊的一半。" + tri_svg(30, {"b": "1", "a": "√3", "c": "2"})],
        [example("等腰直角三角形斜邊 10，股長？", ["10 ÷ √2 ＝ 5√2。"], "5√2"),
         example("30°-60°-90°，斜邊 8，兩股？", ["最短邊 8 ÷ 2 ＝ 4。", "另一股 4√3。"], "4、4√3")],
        [("30° 的對邊乘以 √3 得斜邊", "斜邊是最短邊的 2 倍"),
         ("斜邊 10 的等腰直角三角形，股長 10√2", "股比斜邊短：10 ÷ √2 ＝ 5√2"),
         ("把 60° 的對邊當最短邊", "最短邊是 30° 的對邊")])
    faq = [{"q": "為什麼 30°-60°-90° 的最短邊是斜邊的一半？",
            "a": "把兩個這樣的三角形沿長股拼起來，會變成正三角形，斜邊是正三角形的邊，最短邊是它的一半。"},
           {"q": "這兩種邊長比要怎麼記？",
            "a": "45° 的是 1：1：√2（正方形對角線），30°-60° 的是 1：√3：2（正三角形切一半），小的角對小的邊。"},
           {"q": "九年級的特殊直角三角形要學什麼？",
            "a": "108課綱 S-9-4：相似直角三角形邊長比值的不變性，30°-60°-90° 的邊長比 1：√3：2，45°-45°-90° 的邊長比 1：1：√2。"}]
    make_unit(R, "grade-9", "special-right-triangles", "S-9-4",
              "相似直角三角形邊長比值的不變性：直角三角形中某一銳角的角度決定邊長比值，該比值為不變量，不因相似直角三角形的大小而改變；三內角為30°，60°，90° 其邊長比記錄為「1：√3：2」；三內角為45°，45°，90° 其邊長比記錄為「1：1：√2」。",
              "特殊直角三角形的邊長比",
              "九年級數學 特殊直角三角形 練習題｜1：√3：2・1：1：√2 學習單（附解答）",
              "特殊直角三角形",
              "國中九年級數學「特殊直角三角形的邊長比」免費學習單：45°-45°-90° 的 1：1：√2、30°-60°-90° 的 1：√3：2，由斜邊或股求其他邊，正方形對角線、正三角形的高，梯子與坡道應用題。100題線上練習馬上對答案，附可列印解答。",
              "1：1：√2 和 1：√3：2",
              "30°-60°-90° 的最短邊（30° 的對邊）是斜邊的一半。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
