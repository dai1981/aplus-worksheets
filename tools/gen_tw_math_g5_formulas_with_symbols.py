# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：以符號表示數學公式（108課綱 R-5-3）
  python3 tools/gen_tw_math_g5_formulas_with_symbols.py
面積・周長・體積の公式を文字と記號（□・△・○）で表す、代入して求める、公式から逆に求める、生活の公式（總價・找錢）。
誤答：周長と面積の公式を取り違える、三角形の ÷ 2 を忘れる、梯形で上底＋下底の括號を忘れる。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(51026)
NM = Names(R)

F = [("長方形的面積", "長 × 寬", ["（長 ＋ 寬）× 2", "長 ＋ 寬", "長 × 寬 ÷ 2"]),
     ("長方形的周長", "（長 ＋ 寬）× 2", ["長 × 寬", "長 ＋ 寬 × 2", "長 × 寬 × 2"]),
     ("正方形的面積", "邊長 × 邊長", ["邊長 × 4", "邊長 ＋ 邊長", "邊長 × 2"]),
     ("正方形的周長", "邊長 × 4", ["邊長 × 邊長", "邊長 × 2", "邊長 ＋ 4"]),
     ("三角形的面積", "底 × 高 ÷ 2", ["底 × 高", "（底 ＋ 高）× 2", "底 ＋ 高 ÷ 2"]),
     ("平行四邊形的面積", "底 × 高", ["底 × 高 ÷ 2", "（底 ＋ 高）× 2", "底 × 斜邊"]),
     ("梯形的面積", "（上底 ＋ 下底）× 高 ÷ 2", ["上底 ＋ 下底 × 高 ÷ 2", "上底 × 下底 × 高", "（上底 ＋ 下底）× 高"]),
     ("長方體的體積", "長 × 寬 × 高", ["（長 ＋ 寬 ＋ 高）× 4", "長 × 寬", "長 ＋ 寬 ＋ 高"]),
     ("正方體的體積", "邊長 × 邊長 × 邊長", ["邊長 × 6", "邊長 × 邊長 × 6", "邊長 × 12"]),
     ("菱形的面積", "對角線 × 對角線 ÷ 2", ["對角線 × 對角線", "邊長 × 4", "對角線 ＋ 對角線"])]


def s1(seen):
    out = []
    for name, ans, w in F:
        out.append(mcq("%s公式是哪一個？" % name, ans, w, "%s ＝%s%s。" % (name, "" if ans.startswith("（") else " ", ans)))
    rev = [("長 × 寬", "長方形的面積", ["長方形的周長", "長方體的體積", "三角形的面積"]),
           ("邊長 × 4", "正方形的周長", ["正方形的面積", "正方體的體積", "長方形的周長"]),
           ("底 × 高 ÷ 2", "三角形的面積", ["平行四邊形的面積", "梯形的面積", "長方形的周長"]),
           ("底 × 高", "平行四邊形的面積", ["三角形的面積", "梯形的面積", "正方形的周長"]),
           ("（上底 ＋ 下底）× 高 ÷ 2", "梯形的面積", ["三角形的面積", "平行四邊形的面積", "長方形的周長"]),
           ("長 × 寬 × 高", "長方體的體積", ["長方形的面積", "正方體的表面積", "長方形的周長"]),
           ("（長 ＋ 寬）× 2", "長方形的周長", ["長方形的面積", "正方形的周長", "三角形的面積"]),
           ("邊長 × 邊長 × 邊長", "正方體的體積", ["正方形的面積", "正方形的周長", "長方體的表面積"]),
           ("邊長 × 邊長", "正方形的面積", ["正方形的周長", "正方體的體積", "長方形的周長"]),
           ("邊長 × 邊長 × 6", "正方體的表面積", ["正方體的體積", "正方形的面積", "正方形的周長"])]
    for f, ans, w in rev:
        out.append(mcq("「%s」是哪一個圖形的什麼公式？" % f, ans, w, "%s ＝ %s。" % (ans, f)))
    for o in out:
        seen.add(o["q"])
    return out


SYM = ["□", "△", "○"]


def s2(seen):
    def mk():
        k = R.choice(["sq_p", "sq_a", "rect_a", "rect_p", "tri", "box", "cube", "para"])
        a, b, c = R.sample(SYM, 3)
        if k == "sq_p":
            q = "正方形的邊長是 %s 公分，周長怎麼用符號表示？" % a
            ans, w = "%s × 4" % a, ["%s × %s" % (a, a), "%s ＋ 4" % a, "%s × 2" % a]
        elif k == "sq_a":
            q = "正方形的邊長是 %s 公分，面積怎麼用符號表示？" % a
            ans, w = "%s × %s" % (a, a), ["%s × 4" % a, "%s × 2" % a, "%s ＋ %s" % (a, a)]
        elif k == "rect_a":
            q = "長方形的長是 %s 公分，寬是 %s 公分，面積怎麼用符號表示？" % (a, b)
            ans, w = "%s × %s" % (a, b), ["（%s ＋ %s）× 2" % (a, b), "%s ＋ %s" % (a, b), "%s × %s ÷ 2" % (a, b)]
        elif k == "rect_p":
            q = "長方形的長是 %s 公分，寬是 %s 公分，周長怎麼用符號表示？" % (a, b)
            ans, w = "（%s ＋ %s）× 2" % (a, b), ["%s × %s" % (a, b), "%s ＋ %s × 2" % (a, b), "%s × %s × 2" % (a, b)]
        elif k == "tri":
            q = "三角形的底是 %s 公分，高是 %s 公分，面積怎麼用符號表示？" % (a, b)
            ans, w = "%s × %s ÷ 2" % (a, b), ["%s × %s" % (a, b), "%s ＋ %s ÷ 2" % (a, b), "（%s ＋ %s）× 2" % (a, b)]
        elif k == "para":
            q = "平行四邊形的底是 %s 公分，高是 %s 公分，面積怎麼用符號表示？" % (a, b)
            ans, w = "%s × %s" % (a, b), ["%s × %s ÷ 2" % (a, b), "（%s ＋ %s）× 2" % (a, b), "%s ＋ %s" % (a, b)]
        elif k == "box":
            q = "長方體的長、寬、高分別是 %s、%s、%s 公分，體積怎麼用符號表示？" % (a, b, c)
            ans, w = "%s × %s × %s" % (a, b, c), ["%s ＋ %s ＋ %s" % (a, b, c), "（%s ＋ %s ＋ %s）× 4" % (a, b, c), "%s × %s" % (a, b)]
        else:
            q = "正方體的邊長是 %s 公分，體積怎麼用符號表示？" % a
            ans, w = "%s × %s × %s" % (a, a, a), ["%s × 6" % a, "%s × 12" % a, "%s × %s × 6" % (a, a)]
        return mcq(q, ans, w, "把公式裡的數換成符號：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice(["rect_p", "tri", "trap", "box", "sq_a", "para"])
        if k == "rect_p":
            a, b = R.randint(8, 40), R.randint(3, 25)
            if a <= b:
                return None
            q = "長方形周長 ＝（□ ＋ △）× 2。當 □ ＝ %d、△ ＝ %d 時，周長是多少公分？" % (a, b)
            v, w = (a + b) * 2, [a * b, a + b * 2, a + b]
            ex = "（%d ＋ %d）× 2" % (a, b)
        elif k == "tri":
            a, b = R.randint(4, 30), R.randint(4, 30)
            if (a * b) % 2:
                return None
            q = "三角形面積 ＝ □ × △ ÷ 2。當底 □ ＝ %d、高 △ ＝ %d 時，面積是多少平方公分？" % (a, b)
            v, w = a * b // 2, [a * b, (a + b) * 2, a * b // 2 + a]
            ex = "%d × %d ÷ 2" % (a, b)
        elif k == "trap":
            a, b, h = R.randint(3, 15), R.randint(6, 25), R.randint(4, 16)
            if a >= b or ((a + b) * h) % 2:
                return None
            q = "梯形面積 ＝（□ ＋ ○）× △ ÷ 2。當上底 □ ＝ %d、下底 ○ ＝ %d、高 △ ＝ %d 時，面積是多少平方公分？" % (a, b, h)
            ex = "（%d ＋ %d）× %d ÷ 2" % (a, b, h)
            v, w = (a + b) * h // 2, [(a + b) * h, a + b * h // 2 if (b * h) % 2 == 0 else v + h, a * b * h // 2 if (a * b * h) % 2 == 0 else v - h]
        elif k == "box":
            a, b, c = R.randint(3, 15), R.randint(2, 10), R.randint(2, 12)
            q = "長方體體積 ＝ □ × △ × ○。當 □ ＝ %d、△ ＝ %d、○ ＝ %d 時，體積是多少立方公分？" % (a, b, c)
            v, w = a * b * c, [a + b + c, a * b, (a + b + c) * 4]
            ex = "%d × %d × %d" % (a, b, c)
        elif k == "sq_a":
            a = R.randint(6, 30)
            q = "正方形面積 ＝ □ × □。當 □ ＝ %d 時，面積是多少平方公分？" % a
            v, w = a * a, [a * 4, a * 2, a * a + a]
            ex = "%d × %d" % (a, a)
        else:
            a, b = R.randint(6, 40), R.randint(4, 25)
            q = "平行四邊形面積 ＝ □ × △。當底 □ ＝ %d、高 △ ＝ %d 時，面積是多少平方公分？" % (a, b)
            v, w = a * b, [a * b // 2 if (a * b) % 2 == 0 else a * b + a, (a + b) * 2, a + b]
            ex = "%d × %d" % (a, b)
        return mcq(q, num(v), [num(x) for x in w if x != v], "把數放進符號的位置：%s ＝ %s。" % (ex, num(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        k = R.choice(["rect_w", "tri_h", "sq_s", "box_h", "para_b"])
        if k == "rect_w":
            a, b = R.randint(8, 30), R.randint(3, 20)
            q = "長方形面積 ＝ 長 × □。長是 %d 公分，面積是 %d 平方公分，寬 □ 是多少公分？" % (a, a * b)
            v, w = b, [a * b - a, a * b * a, b + 2]
            ex = "%d ÷ %d" % (a * b, a)
        elif k == "tri_h":
            a, b = R.randint(4, 20), R.randint(3, 20)
            if (a * b) % 2:
                return None
            ar = a * b // 2
            q = "三角形面積 ＝ 底 × □ ÷ 2。底是 %d 公分，面積是 %d 平方公分，高 □ 是多少公分？" % (a, ar)
            ex = "%d × 2 ÷ %d" % (ar, a)
            v, w = b, [ar // a if ar % a == 0 and ar // a != b else b // 2 if b % 2 == 0 and b // 2 != 0 else b + 3, ar * 2, ar - a if ar > a else b + 1]
        elif k == "sq_s":
            s = R.randint(3, 15)
            q = "正方形周長 ＝ □ × 4。周長是 %d 公分，邊長 □ 是多少公分？" % (s * 4)
            v, w = s, [s * 16, s * 4 - 4, s * 2]
            ex = "%d ÷ 4" % (s * 4)
        elif k == "box_h":
            a, b, c = R.randint(3, 12), R.randint(2, 10), R.randint(2, 10)
            q = "長方體體積 ＝ 長 × 寬 × □。長 %d 公分、寬 %d 公分，體積 %d 立方公分，高 □ 是多少公分？" % (a, b, a * b * c)
            v, w = c, [a * b * c - a - b, a * b, c + 1]
            ex = "%d ÷（%d × %d）" % (a * b * c, a, b)
        else:
            a, b = R.randint(5, 30), R.randint(3, 20)
            q = "平行四邊形面積 ＝ □ × 高。高是 %d 公分，面積是 %d 平方公分，底 □ 是多少公分？" % (b, a * b)
            v, w = a, [a * b - b, a * 2, a + 1]
            ex = "%d ÷ %d" % (a * b, b)
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in w if x != v and x > 0], "用除法把 □ 找回來：□ ＝ %s ＝ %d（公分）。" % (ex, v))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def price():
        item, p = R.choice([(("鉛筆", "枝"), 12), (("鉛筆", "枝"), 15), (("筆記本", "本"), 35), (("筆記本", "本"), 45), (("麵包", "個"), 25), (("麵包", "個"), 30), (("果汁", "瓶"), 20), (("果汁", "瓶"), 25)])
        q = "一%s%s %d 元，買 □ %s要付 △ 元。△ 和 □ 的關係是哪一個？" % (item[1], item[0], p, item[1])
        return mcq(q, "△ ＝ %d × □" % p, ["□ ＝ %d × △" % p, "△ ＝ %d ＋ □" % p, "△ ＝ □ ÷ %d" % p], "總價 ＝ 單價 × 數量：△ ＝ %d × □。" % p)

    def change():
        p = R.choice([12, 18, 25, 30, 45])
        m = R.choice([100, 500])
        n = R.randint(2, min(12, m // p - 1)) if m // p - 1 >= 2 else 2
        if p * n >= m:
            return None
        q = "一枝筆 %d 元。付 %d 元買 □ 枝，找回 ○ 元，○ ＝ %d － %d × □。當 □ ＝ %d 時，○ 是多少元？" % (p, m, m, p, n)
        v = m - p * n
        return mcq(q, "%d 元" % v, ["%d 元" % x for x in (p * n, m - p - n if m - p - n != v else v + p, v + p, m - n) if x != v and x > 0],
                   "○ ＝ %d － %d × %d ＝ %d － %d ＝ %d（元）。" % (m, p, n, m, p * n, v))

    def age():
        d = R.randint(24, 35)
        who = NM.next()
        x = R.randint(8, 12)
        q = "%s的媽媽比%s大 %d 歲。%s □ 歲時，媽媽 △ 歲，△ ＝ □ ＋ %d。當 □ ＝ %d 時，△ 是多少？" % (who, who, d, who, d, x)
        return mcq(q, "%d 歲" % (x + d), ["%d 歲" % y for y in (d - x, x * d if x * d < 99 else d + 2 * x, d)], "△ ＝ %d ＋ %d ＝ %d（歲）。" % (x, d, x + d))
    return pick_unique(R, price, 7, seen) + pick_unique(R, change, 7, seen) + pick_unique(R, age, 6, seen)


def main():
    seen = set()
    sets = [("認識公式", s1(seen)), ("用符號寫公式", s2(seen)), ("把數放進公式", s3(seen)),
            ("用公式求未知的數", s4(seen)), ("生活中的公式", s5(seen))]
    body = lesson(
        ["<b>公式</b>把算法寫成一句話，例如：長方形面積 ＝ 長 × 寬。",
         "可以用 <b>□、△、○</b> 這些符號代表數：長是 □、寬是 △，面積 ＝ □ × △。",
         "知道符號是多少，就把數放進去算；知道答案，可以用除法把 □ 找回來。"],
        [example("三角形面積 ＝ □ × △ ÷ 2，□ ＝ 12、△ ＝ 7", ["12 × 7 ÷ 2 ＝ 84 ÷ 2。"], "42 平方公分"),
         example("長方形面積 ＝ 9 × □ ＝ 72，□ 是多少？", ["□ ＝ 72 ÷ 9。"], "8 公分")],
        [("正方形周長寫成 □ × □", "周長是 4 條邊：□ × 4"),
         ("三角形面積寫成 □ × △", "要再 ÷ 2"),
         ("梯形面積寫成 □ ＋ ○ × △ ÷ 2", "上底加下底要加括號：（□ ＋ ○）× △ ÷ 2")])
    faq = [{"q": "為什麼要用符號表示公式？",
            "a": "符號可以代表任何數，一個公式就能算所有大小的圖形。108課綱 R-5-3 是國中代數的前置經驗，讓孩子初步體驗「符號代表數」。"},
           {"q": "五年級要會哪些公式？",
            "a": "長方形和正方形的周長、面積，三角形、平行四邊形、梯形的面積，長方體和正方體的體積，以及總價 ＝ 單價 × 數量這類生活中的公式。"},
           {"q": "知道面積，怎麼求高？",
            "a": "把公式反過來用除法：例如三角形面積 ＝ 底 × 高 ÷ 2，高 ＝ 面積 × 2 ÷ 底。"}]
    make_unit(R, "grade-5", "formulas-with-symbols", "R-5-3",
              "以符號表示數學公式：國中代數的前置經驗。初步體驗符號之使用，隱含「符號代表數」的意義。",
              "以符號表示數學公式",
              "五年級數學 用符號表示公式 練習題｜面積・周長・體積公式 學習單（附解答）",
              "符號與公式",
              "國小五年級數學「以符號表示數學公式」免費學習單：認識面積、周長、體積公式，用 □、△、○ 寫公式，把數放進公式計算、用公式求未知的數和生活中的公式。100題線上練習馬上對答案，附可列印解答。",
              "符號可以代表數",
              "長方形面積 ＝ □ × △，□ 是長、△ 是寬。",
              body, faq, sets, 26)


if __name__ == "__main__":
    main()
