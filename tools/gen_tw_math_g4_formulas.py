# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：以文字表示數學公式（108課綱 R-4-3）
  python3 tools/gen_tw_math_g4_formulas.py
文字の公式（長方形の周長・面積、正方形、總價＝單價×數量、找回的錢、平分）を選ぶ・使う・逆に使う。
誤答：周長＝長＋寬、面積と周長の公式の取り違え、逆算で掛けてしまう。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41022)
NM = Names(R)

FORM = [("長方形的周長", "（長 ＋ 寬）× 2", ["長 ＋ 寬", "長 × 寬", "長 × 2 ＋ 寬"]),
        ("長方形的面積", "長 × 寬", ["（長 ＋ 寬）× 2", "長 ＋ 寬", "長 × 寬 × 2"]),
        ("正方形的周長", "邊長 × 4", ["邊長 × 邊長", "邊長 × 2", "邊長 ＋ 4"]),
        ("正方形的面積", "邊長 × 邊長", ["邊長 × 4", "邊長 ＋ 邊長", "邊長 × 2"]),
        ("買東西的總價", "單價 × 數量", ["單價 ＋ 數量", "總價 ÷ 數量", "單價 ÷ 數量"]),
        ("找回的錢", "付的錢 － 總價", ["總價 － 付的錢", "付的錢 ＋ 總價", "付的錢 × 總價"]),
        ("平分後每份的數量", "總數 ÷ 份數", ["總數 × 份數", "份數 ÷ 總數", "總數 － 份數"]),
        ("單價（一個多少元）", "總價 ÷ 數量", ["總價 × 數量", "數量 ÷ 總價", "總價 － 數量"]),
        ("正三角形的周長", "邊長 × 3", ["邊長 × 4", "邊長 × 2", "邊長 ＋ 3"]),
        ("長方形的寬（知道面積和長）", "面積 ÷ 長", ["面積 × 長", "面積 － 長", "長 ÷ 面積"])]


def s1(seen):
    out = []
    for name, f, w in FORM:
        out.append(mcq("用文字表示：%s ＝ ？" % name, f, w, "%s ＝ %s。" % (name, f)))
    for o in out:
        seen.add(o["q"])

    def back():
        name, f, w = R.choice(FORM[:4])
        q = "「%s」是哪一個圖形的什麼公式？" % f
        return mcq(q, name, [n for n, ff, ww in FORM[:4] if n != name][:3], "%s ＝ %s。" % (name, f))
    return out + pick_unique(R, back, 4, seen) + [mcq(*x) for x in [
        ("公式「總價 ＝ 單價 × 數量」中，單價 25 元、數量 6，總價是多少？", "150 元", ["31 元", "19 元", "125 元"], "25 × 6 ＝ 150（元）。"),
        ("公式「找回的錢 ＝ 付的錢 － 總價」中，付 500 元、總價 368 元，找回多少？", "132 元", ["868 元", "232 元", "142 元"], "500 － 368 ＝ 132（元）。"),
        ("公式「每份 ＝ 總數 ÷ 份數」中，總數 96、份數 8，每份是多少？", "12", ["88", "104", "768"], "96 ÷ 8 ＝ 12。"),
        ("公式「長方形面積 ＝ 長 × 寬」中，長 14、寬 9，面積是多少？", "126", ["23", "46", "116"], "14 × 9 ＝ 126。"),
        ("公式「正方形周長 ＝ 邊長 × 4」中，邊長 17，周長是多少？", "68", ["21", "289", "34"], "17 × 4 ＝ 68。"),
        ("公式「長方形周長 ＝（長 ＋ 寬）× 2」中，長 15、寬 8，周長是多少？", "46", ["23", "120", "38"], "（15 ＋ 8）× 2 ＝ 46。")]]


def s2(seen):
    def rect():
        w, h = R.randint(5, 40), R.randint(3, 30)
        if w == h:
            return None
        ask = R.choice(["周長", "面積"])
        q = "用公式算：長方形的長 %d 公分、寬 %d 公分，%s是多少？" % (w, h, ask)
        if ask == "周長":
            v = 2 * (w + h)
            return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (w + h, w * h if w * h != v else v + 2, 2 * w + h)], "周長 ＝（長 ＋ 寬）× 2 ＝（%d ＋ %d）× 2 ＝ %d（公分）。" % (w, h, v))
        v = w * h
        return mcq(q, "%s 平方公分" % num(v), ["%s 平方公分" % num(x) for x in (2 * (w + h) if 2 * (w + h) != v else v + w, w + h, v + h)], "面積 ＝ 長 × 寬 ＝ %d × %d ＝ %s（平方公分）。" % (w, h, num(v)))

    def price():
        p, n = R.randint(12, 150), R.randint(3, 25)
        q = "用公式「總價 ＝ 單價 × 數量」算：一本 %d 元的書，買 %d 本要多少元？" % (p, n)
        v = p * n
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (p + n, v + p, v - p)], "總價 ＝ %d × %d ＝ %s（元）。" % (p, n, num(v)))
    return pick_unique(R, rect, 12, seen) + pick_unique(R, price, 8, seen)


def s3(seen):
    def width():
        w, h = R.randint(5, 30), R.randint(3, 20)
        A = w * h
        q = "長方形面積 ＝ 長 × 寬。面積 %d 平方公分、長 %d 公分，寬是多少？" % (A, w)
        return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (A - w, A * w if A * w < 5000 else A + w, h + 1, w) if x != h], "寬 ＝ 面積 ÷ 長 ＝ %d ÷ %d ＝ %d（公分）。" % (A, w, h))

    def side():
        a = R.randint(4, 40)
        q = "正方形周長 ＝ 邊長 × 4。周長 %d 公分，邊長是多少？" % (4 * a)
        return mcq(q, "%d 公分" % a, ["%d 公分" % x for x in (4 * a * 4, 2 * a, a + 4, 4 * a - 4)], "邊長 ＝ 周長 ÷ 4 ＝ %d ÷ 4 ＝ %d（公分）。" % (4 * a, a))

    def unit():
        p, n = R.randint(12, 90), R.randint(3, 15)
        q = "總價 ＝ 單價 × 數量。買 %d 個一樣的便當一共 %s 元，一個多少元？" % (n, num(p * n))
        return mcq(q, "%d 元" % p, ["%d 元" % x for x in (p * n * n if p * n * n < 10000 else p + n, p * n - n, p + 1)], "單價 ＝ 總價 ÷ 數量 ＝ %s ÷ %d ＝ %d（元）。" % (num(p * n), n, p))

    def per():
        w, h = R.randint(5, 30), R.randint(3, 20)
        if w == h:
            return None
        P = 2 * (w + h)
        q = "長方形周長 ＝（長 ＋ 寬）× 2。周長 %d 公分、長 %d 公分，寬是多少？" % (P, w)
        return mcq(q, "%d 公分" % h, ["%d 公分" % x for x in (P - w, P // 2, P - 2 * w if P - 2 * w > 0 and P - 2 * w != h else h + 2) if x != h], "長 ＋ 寬 ＝ %d ÷ 2 ＝ %d，寬 ＝ %d － %d ＝ %d（公分）。" % (P, P // 2, P // 2, w, h))
    return pick_unique(R, width, 5, seen) + pick_unique(R, side, 5, seen) + pick_unique(R, unit, 5, seen) + pick_unique(R, per, 5, seen)


def s4(seen):
    def table_q():
        p = R.randint(15, 60)
        ns = sorted(R.sample(range(2, 12), 3))
        k = R.randint(0, 2)
        cells = ["%d" % (p * n) if i != k else "？" for i, n in enumerate(ns)]
        q = "一枝筆 %d 元。數量和總價的關係如下：數量 %s 枝，總價 %s 元。「？」是多少？" % (p, "、".join(str(n) for n in ns), "、".join(cells))
        v = p * ns[k]
        return mcq(q, num(v), [num(x) for x in (p + ns[k], v + p, v - p)], "總價 ＝ 單價 × 數量 ＝ %d × %d ＝ %s（元）。" % (p, ns[k], num(v)))

    def which():
        F = [("小明說：「長方形的周長 ＝ 長 ＋ 寬」，對嗎？", "不對，要（長 ＋ 寬）× 2", ["對", "不對，要 長 × 寬", "不對，要 長 × 寬 × 2"], "長和寬各有 2 條，周長 ＝（長 ＋ 寬）× 2。"),
             ("小美說：「正方形的面積 ＝ 邊長 × 4」，對嗎？", "不對，要 邊長 × 邊長", ["對", "不對，要 邊長 × 2", "不對，要 邊長 ＋ 4"], "邊長 × 4 是周長；面積是 邊長 × 邊長。"),
             ("「單價 ＝ 總價 ÷ 數量」可以由哪一個公式得到？", "總價 ＝ 單價 × 數量", ["總價 ＝ 單價 ＋ 數量", "數量 ＝ 單價 × 總價", "總價 ＝ 數量 － 單價"], "乘法和除法互逆：總價 ＝ 單價 × 數量，所以 單價 ＝ 總價 ÷ 數量。"),
             ("「寬 ＝ 面積 ÷ 長」可以由哪一個公式得到？", "面積 ＝ 長 × 寬", ["周長 ＝ 長 ＋ 寬", "面積 ＝ 長 ＋ 寬", "長 ＝ 面積 × 寬"], "面積 ＝ 長 × 寬，所以 寬 ＝ 面積 ÷ 長。")]
        return mcq(*R.choice(F))
    return pick_unique(R, table_q, 16, seen) + pick_unique(R, which, 4, seen)


def s5(seen):
    def mk():
        k = R.choice(["fence", "tile", "shop", "paint"])
        who = NM.next()
        if k == "fence":
            w, h, p = R.randint(5, 20), R.randint(3, 15), R.choice([20, 30, 50])
            if w == h:
                return None
            P = 2 * (w + h)
            q = "長 %d 公尺、寬 %d 公尺的花園，四周圍上籬笆，每公尺 %d 元，一共要多少元？" % (w, h, p)
            v = P * p
            return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in ((w + h) * p, w * h * p, P + p)], "周長（%d ＋ %d）× 2 ＝ %d 公尺，總價 %d × %d ＝ %s（元）。" % (w, h, P, P, p, num(v)))
        if k == "tile":
            w, h = R.randint(3, 12), R.randint(2, 10)
            p = R.choice([200, 300, 500])
            q = "長 %d 公尺、寬 %d 公尺的地板鋪木地板，每平方公尺 %d 元，一共要多少元？" % (w, h, p)
            v = w * h * p
            return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (2 * (w + h) * p, (w + h) * p, w * h + p)], "面積 %d × %d ＝ %d 平方公尺，總價 %d × %d ＝ %s（元）。" % (w, h, w * h, w * h, p, num(v)))
        if k == "shop":
            p, n, m = R.randint(20, 80), R.randint(3, 9), R.choice([500, 1000])
            q = "%s買 %d 個 %d 元的飯糰，付 %d 元，找回多少元？" % (who, n, p, m)
            v = m - p * n
            return mcq(q, "%d 元" % v, ["%d 元" % x for x in (p * n, m - p - n, v + p)], "總價 %d × %d ＝ %d，找回 %d － %d ＝ %d（元）。" % (p, n, p * n, m, p * n, v))
        a = R.randint(3, 12)
        p = R.choice([120, 150, 180])
        q = "邊長 %d 公尺的正方形牆面要油漆，每平方公尺的油漆費是 %d 元，一共要多少元？" % (a, p)
        v = a * a * p
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (4 * a * p, a * p, a * a + p, 2 * a * p)], "面積 %d × %d ＝ %d 平方公尺，%d × %d ＝ %s（元）。" % (a, a, a * a, a * a, p, num(v)))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("認識文字公式", s1(seen)), ("用公式計算", s2(seen)), ("公式反過來用", s3(seen)),
            ("公式和表格", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["用文字和運算符號寫出來的算法，叫做<b>公式</b>：長方形面積 ＝ 長 × 寬，總價 ＝ 單價 × 數量。",
         "用公式時，把數字放進對應的文字裡再計算。",
         "公式可以反過來用：面積 ＝ 長 × 寬，所以 寬 ＝ 面積 ÷ 長；總價 ＝ 單價 × 數量，所以 單價 ＝ 總價 ÷ 數量。"],
        [example("長方形周長 ＝（長 ＋ 寬）× 2，長 12、寬 7，周長是多少？", ["（12 ＋ 7）× 2。", "＝ 19 × 2 ＝ 38。"], "38"),
         example("面積 72 平方公分、長 9 公分的長方形，寬是多少？", ["寬 ＝ 面積 ÷ 長。", "72 ÷ 9 ＝ 8。"], "8 公分")],
        [("長方形周長 ＝ 長 ＋ 寬", "（長 ＋ 寬）× 2"),
         ("正方形面積 ＝ 邊長 × 4", "邊長 × 4 是周長；面積 ＝ 邊長 × 邊長"),
         ("求寬時用 面積 × 長", "反過來用要用除法：寬 ＝ 面積 ÷ 長")])
    faq = [{"q": "四年級的「以文字表示公式」要學什麼？",
            "a": "108課綱 R-4-3：理解用文字和運算符號一起表示的數學公式，例如面積、周長、總價的公式，並能應用。"},
           {"q": "公式反過來用是什麼意思？",
            "a": "利用乘除互逆：面積 ＝ 長 × 寬，知道面積和長，就可以用 寬 ＝ 面積 ÷ 長 求出寬。"},
           {"q": "學文字公式有什麼用？",
            "a": "公式是代數的基礎，五、六年級會用符號（像 □ 或 x）代替文字，國中再學更多公式。"}]
    make_unit(R, "grade-4", "formulas", "R-4-3",
              "以文字表示數學公式：理解以文字和運算符號聯合表示的數學公式，並能應用公式。",
              "以文字表示公式：周長、面積、總價",
              "四年級數學 文字公式 練習題｜周長面積公式・總價公式・公式反過來用 學習單（附解答）",
              "文字公式",
              "國小四年級數學「以文字表示公式」免費學習單：認識周長、面積、總價、找錢的文字公式，用公式計算、公式反過來用和應用題。100題線上練習馬上對答案，附可列印解答。",
              "把數字放進公式裡的文字",
              "公式可以反過來用：寬 ＝ 面積 ÷ 長。",
              body, faq, sets, 22)


if __name__ == "__main__":
    main()
