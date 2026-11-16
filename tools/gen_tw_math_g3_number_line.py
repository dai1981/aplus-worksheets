# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：整數數線（108課綱 N-3-11）
  python3 tools/gen_tw_math_g3_number_line.py
數線の報讀（1格＝1、10、100）、標示、比大小、在數線上做加減、生活中的數線。
誤答：1格を1と数える（1格＝10なのに）、目盛りを1つずらす、端の目盛りから数え始める。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, INK, RED, BLUE

R = random.Random(31011)
NM = Names(R)

X0, X1 = 30, 490


def nline(start, step, n, labels, marks=(), jump=None):
    """start から step ずつ n 格の數線。labels：數字を書く目盛り番号、marks：[(番号, 文字, 色)]、jump：(from, to)"""
    gap = (X1 - X0) / n
    s = [line(X0 - 12, 50, X1 + 14, 50, INK, 2),
         "<polygon points='%d,44 %d,50 %d,56' fill='%s'/>" % (X1 + 14, X1 + 24, X1 + 14, INK)]
    for i in range(n + 1):
        x = X0 + i * gap
        s.append(line(x, 42, x, 58, INK, 2))
        if i in labels:
            s.append(text(x, 80, num(start + i * step), 15))
    for i, t, col in marks:
        x = X0 + i * gap
        s.append("<polygon points='%.1f,38 %.1f,24 %.1f,24' fill='%s'/>" % (x, x - 7, x + 7, col))
        s.append(text(x, 18, t, 15, col=col))
    if jump:
        a, b = jump
        xa, xb = X0 + a * gap, X0 + b * gap
        s.append("<path d='M%.1f 40 Q%.1f %d %.1f 40' fill='none' stroke='%s' stroke-width='2.5'/>" % (xa, (xa + xb) / 2, 2, xb, BLUE))
        d = 1 if xb > xa else -1
        s.append("<polygon points='%.1f,40 %.1f,30 %.1f,36' fill='%s'/>" % (xb, xb - 9 * d, xb - 2 * d, BLUE))
    return fig(svg_wrap(520, 92, "".join(s), "數線"))


def s1(seen):
    """1格＝1"""
    def mk():
        start = R.choice([0, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
        k = R.randint(1, 9)
        if k == 5:
            return None
        v = start + k
        q = "數線上箭頭指的數是多少？" + nline(start, 1, 10, (0, 5, 10), [(k, "?", RED)])
        return mcq(q, num(v), [num(x) for x in (v + 1, v - 1, start + 10 - k, k, v + 10)],
                   "1 格是 1，從 %d 往右數 %d 格，是 %d。" % (start, k, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    """1格＝10、100、5、2"""
    def mk():
        step = R.choice([10, 10, 100, 100, 5, 2])
        n = 10
        start = R.choice([0, 0, step * 10, step * 20]) if step >= 10 else R.choice([0, step * 10])
        k = R.randint(1, 9)
        if k == 5:
            return None
        v = start + k * step
        q = ("數線上箭頭指的數是多少？" + nline(start, step, n, (0, 5, 10), [(k, "?", RED)]))
        return mcq(q, num(v), [num(x) for x in (start + k, v + step, v - step, k * step if start else v * 10, start + 10 * step - k * step)],
                   "從 %s 到 %s 有 5 格，1 格是 %d。從 %s 往右 %d 格：%s。" % (
                       num(start), num(start + 5 * step), step, num(start), k, num(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mark():
        step = R.choice([1, 10, 100])
        start = R.choice([0, step * 10]) if step > 1 else R.choice([0, 20, 40])
        a, b = R.sample([i for i in range(1, 10) if i != 5], 2)
        va, vb = start + a * step, start + b * step
        ans = "甲" if va > vb else "乙"
        q = "甲、乙兩個數，哪一個比較大？" + nline(start, step, 10, (0, 5, 10), [(a, "甲", RED), (b, "乙", BLUE)])
        return mcq(q, ans + "（%s）" % num(max(va, vb)),
                   [("乙" if ans == "甲" else "甲") + "（%s）" % num(min(va, vb)), "一樣大", ans + "（%s）" % num(max(va, vb) + step)],
                   "甲是 %s，乙是 %s。數線上越右邊的數越大。" % (num(va), num(vb)))

    def dist():
        step = R.choice([1, 10, 100])
        start = 0 if step > 1 else R.choice([0, 10, 20])
        a, b = sorted(R.sample(range(1, 10), 2))
        if b - a < 2:
            return None
        va, vb = start + a * step, start + b * step
        q = "甲和乙相差多少？" + nline(start, step, 10, (0, 5, 10), [(a, "甲", RED), (b, "乙", BLUE)])
        d = vb - va
        return mcq(q, num(d), [num(x) for x in (b - a, d + step, d - step, va + vb)],
                   "甲是 %s，乙是 %s，%s － %s ＝ %s。（中間有 %d 格）" % (num(va), num(vb), num(vb), num(va), num(d), b - a))
    return pick_unique(R, mark, 10, seen) + pick_unique(R, dist, 10, seen)


def s4(seen):
    def mk():
        step = R.choice([1, 1, 10, 100])
        a = R.randint(1, 8)
        add = R.random() < .55
        b = R.randint(2, 10 - a) if add else R.randint(2, a) if a >= 2 else None
        if b is None or (add and a + b > 10) or (not add and a - b < 0):
            return None
        to = a + b if add else a - b
        va, vb, vt = a * step, b * step, to * step
        sign = "＋" if add else "－"
        q = "看數線，%s %s %s ＝？" % (num(va), sign, num(vb)) + nline(0, step, 10, (0, 5, 10), (), (a, to))
        w = [num(x) for x in (va - vb if add else va + vb, vt + step, vt - step, to, vt + 2 * step, vt - 2 * step)]
        return mcq(q, num(vt), w, "從 %s %s %d 格（%s），到 %s。" % (
            num(va), "往右跳" if add else "往左跳", b, num(vb), num(vt)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def road():
        step = R.choice([10, 100])
        a = R.randint(2, 8)
        b = R.randint(1, 10 - a)
        if b == 0:
            return None
        who = NM.next()
        unit = "公尺"
        q = ("%s家在 0 的位置，學校在 %s 公尺，公園比學校再遠 %s 公尺。公園在數線上的哪個數？" % (who, num(a * step), num(b * step))
             + nline(0, step, 10, (0, 5, 10), [(a, "學校", RED)]))
        v = (a + b) * step
        return mcq(q, num(v) + " " + unit, [num(x) + " " + unit for x in (b * step, a * step - b * step if a > b else v + step, v + step, v - step)],
                   "學校 %s ＋ %s ＝ %s（公尺）。" % (num(a * step), num(b * step), num(v)))

    def ruler():
        a = R.randint(1, 6)
        b = R.randint(a + 3, 10)
        q = ("一枝鉛筆從尺上的 %d 公分量到 %d 公分，鉛筆長幾公分？" % (a, b)
             + nline(0, 1, 10, tuple(range(11)), [(a, "", RED), (b, "", RED)]))
        return mcq(q, "%d 公分" % (b - a), ["%d 公分" % x for x in (b, b - a + 1, a + b, b - a - 1)],
                   "不是從 0 開始量，要用 %d － %d ＝ %d（公分）。" % (b, a, b - a))

    def temp():
        start = R.choice([0, 100, 200, 300])
        k = R.randint(1, 9)
        m = R.randint(1, 9)
        if k == m or k == 5:
            return None
        who = NM.next()
        q = ("%s集點卡上已經有 %s 點（甲），還要幾點才能到 %s 點（乙）？" % (who, num(start + k * 10), num(start + m * 10)) if m > k else None)
        if q is None:
            return None
        q += nline(start, 10, 10, (0, 5, 10), [(k, "甲", RED), (m, "乙", BLUE)])
        d = (m - k) * 10
        return mcq(q, "%d 點" % d, ["%d 點" % x for x in (m - k, d + 10, d - 10 if d > 10 else d + 20, start + m * 10)],
                   "%s － %s ＝ %d（點），數線上差 %d 格，1 格是 10。" % (num(start + m * 10), num(start + k * 10), d, m - k))
    return pick_unique(R, road, 7, seen) + pick_unique(R, ruler, 6, seen) + pick_unique(R, temp, 7, seen)


def main():
    seen = set()
    sets = [("數線（1格是1）", s1(seen)), ("1格是多少？", s2(seen)), ("比大小和相差多少", s3(seen)),
            ("在數線上加減", s4(seen)), ("生活中的數線", s5(seen))]
    demo = nline(0, 10, 10, (0, 5, 10), [(3, "?", RED)])
    body = lesson(
        ["<b>數線</b>是一條有刻度的直線，從左到右，數越來越大。",
         "先看<b>1格是多少</b>：0 到 50 有 5 格，1 格就是 10。",
         "往右是加，往左是減。兩個數相差多少，就是中間有幾格 × 1格的數。"],
        [example("箭頭指的數是多少？" + demo, ["0 到 50 有 5 格，1 格是 10。", "從 0 往右 3 格：10、20、30。"], "30"),
         example("在數線上算 30 ＋ 40", ["1 格是 10，從 30 往右跳 4 格。", "到 70。"], "70")],
        [("1 格是 10，卻當成 1 格是 1（寫成 3）", "先看標好的數，算出 1 格是多少"),
         ("數格子時把起點也算進去", "數的是「跳了幾格」，不是數刻度線"),
         ("尺從 2 公分量到 9 公分，說長 9 公分", "要相減：9 － 2 ＝ 7 公分")])
    faq = [{"q": "三年級的數線要學什麼？",
            "a": "108課綱 N-3-11：認識數線，會報讀和標示數線上的數，並理解在數線上比大小、做加法和減法的意義。"},
           {"q": "孩子讀數線常常讀錯，怎麼辦？",
            "a": "先找兩個標好的數，算出中間有幾格，得到「1格是多少」，再往右一格一格數。"},
           {"q": "數線和尺有什麼關係？",
            "a": "尺就是一條數線，1 格是 1 公分。量東西時不從 0 開始，就要用後面的數減前面的數。"}]
    make_unit(R, "grade-3", "number-line", "N-3-11",
              "整數數線：認識數線，含報讀與標示。連結數序、長度、尺的經驗，理解在數線上做比較、加、減的意義。",
              "整數數線：報讀、比大小、在數線上加減",
              "三年級數學 數線 練習題｜報讀數線・1格是多少・數線加減 學習單（附解答）",
              "整數數線",
              "國小三年級數學「數線」免費學習單：報讀數線、1格是10或100、比大小、相差多少、在數線上做加減和生活中的數線。100題線上練習馬上對答案，附可列印解答。",
              "先看 1 格是多少，再往右數",
              "數線越右邊越大；往右是加，往左是減。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
