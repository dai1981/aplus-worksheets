# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：平行四邊形（108課綱 S-8-9）
  python3 tools/gen_tw_math_g8_parallelograms.py
對邊相等・對角相等・鄰角互補、對角線互相平分、平行四邊形の判別條件、式で表した邊・角、周長・面積・對角線で分けた三角形の面積。
誤答：鄰角を等しいとする、對角線を等しいとする（長方形だけ）、一組の對邊平行＋もう一組の對邊相等で平行四邊形とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, num
from tw_g7 import tidy_sets

R = random.Random(81023)


def ov(s):
    return "<span class='ov'>%s</span>" % s


def s1(seen):
    def ang():
        a = R.randint(40, 140)
        if a == 90:
            return None
        k = R.choice(["B", "C", "D"])
        v = a if k == "C" else 180 - a
        q = "平行四邊形 ABCD 中，∠A ＝ %d°，∠%s 是多少度？" % (a, k)
        return mcq(q, "%d°" % v, ["%d°" % x for x in (180 - v, 360 - 2 * a if 360 - 2 * a not in (v, 180 - v) and 0 < 360 - 2 * a < 360 else v + 10, 90 - v // 2 if v < 180 else v - 10)], ("∠C 和 ∠A 是對角，對角相等：%d°。" % a) if k == "C" else "∠%s 和 ∠A 相鄰，鄰角互補：180° － %d° ＝ %d°。" % (k, a, v))

    def side():
        a, b = R.randint(3, 20), R.randint(3, 20)
        if a == b:
            return None
        k = R.choice(["CD", "AD"])
        v = a if k == "CD" else b
        q = "平行四邊形 ABCD 中，%s ＝ %d，%s ＝ %d，%s 是多少？" % (ov("AB"), a, ov("BC"), b, ov(k))
        return mcq(q, str(v), [str(b if v == a else a), str(a + b), str(2 * (a + b))], "對邊相等：%s ＝ %s ＝ %d。" % (ov(k), ov("AB" if k == "CD" else "BC"), v))
    return pick_unique(R, ang, 12, seen) + pick_unique(R, side, 8, seen)


def s2(seen):
    def diag():
        p, q_ = R.randint(3, 20), R.randint(3, 20)
        k = R.choice(["AC", "BD", "OA", "OD"])
        if k == "AC":
            q = "平行四邊形 ABCD 的對角線交於 O，%s ＝ %d，%s 是多少？" % (ov("OA"), p, ov("AC"))
            v, w, e = 2 * p, [p, p + q_, p * p], "對角線互相平分：%s ＝ 2 × %d ＝ %d。" % (ov("AC"), p, 2 * p)
        elif k == "BD":
            q = "平行四邊形 ABCD 的對角線交於 O，%s ＝ %d，%s 是多少？" % (ov("OD"), q_, ov("BD"))
            v, w, e = 2 * q_, [q_, q_ + 2, q_ * q_], "對角線互相平分：%s ＝ 2 × %d ＝ %d。" % (ov("BD"), q_, 2 * q_)
        elif k == "OA":
            q = "平行四邊形 ABCD 的對角線交於 O，%s ＝ %d，%s 是多少？" % (ov("AC"), 2 * p, ov("OC"))
            v, w, e = p, [2 * p, p + 1, 4 * p], "O 是 %s 的中點：%d ÷ 2 ＝ %d。" % (ov("AC"), 2 * p, p)
        else:
            q = "平行四邊形 ABCD 的對角線交於 O，%s ＝ %d，%s ＝ %d，%s 是多少？" % (ov("AC"), 2 * p, ov("BD"), 2 * q_, ov("OB"))
            v, w, e = q_, [p, 2 * q_, p + q_], "O 是 %s 的中點：%d ÷ 2 ＝ %d。" % (ov("BD"), 2 * q_, q_)
        return mcq(q, str(v), [str(x) for x in w] + [str(v + 3)], e)

    def tf():
        facts = [("平行四邊形的對角線一定等長", False, "只有長方形（和正方形）的對角線等長，一般平行四邊形不一定。"),
                 ("平行四邊形的對角線互相平分", True, "兩條對角線的交點是各自的中點。"),
                 ("平行四邊形的對角相等", True, "∠A ＝ ∠C，∠B ＝ ∠D。"),
                 ("平行四邊形的鄰角相等", False, "鄰角互補（和是 180°），不一定相等。"),
                 ("平行四邊形的對角線互相垂直", False, "菱形的對角線才一定互相垂直。"),
                 ("平行四邊形的一條對角線把它分成兩個全等三角形", True, "利用 ASA 或 SSS 可證兩個三角形全等。"),
                 ("平行四邊形是線對稱圖形", False, "一般平行四邊形不是線對稱圖形，是點對稱圖形（對稱中心是對角線交點）。"),
                 ("平行四邊形的兩條對角線把它分成四個面積相等的三角形", True, "四個三角形的底和高關係都一樣，面積都是全部的四分之一。")]
        return facts
    out = []
    for s, ok, why in tf():
        out.append(mcq("「%s」，這句話對嗎？" % s, "對" if ok else "不對", ["不對" if ok else "對", "只有正方形才對", "要看邊長"], why))
    for b in out:
        seen.add(b["q"])
    return out + pick_unique(R, diag, 12, seen)


CONDS = [("兩組對邊分別平行", True, "定義：兩組對邊平行就是平行四邊形。"),
         ("兩組對邊分別相等", True, "兩組對邊相等的四邊形是平行四邊形。"),
         ("兩組對角分別相等", True, "兩組對角相等的四邊形是平行四邊形。"),
         ("兩條對角線互相平分", True, "對角線互相平分的四邊形是平行四邊形。"),
         ("一組對邊平行且相等", True, "一組對邊平行且相等的四邊形是平行四邊形。"),
         ("一組對邊平行，另一組對邊相等", False, "可能是等腰梯形，不一定是平行四邊形。"),
         ("兩條對角線等長", False, "等腰梯形的對角線也等長，不一定是平行四邊形。"),
         ("一組對邊平行", False, "只知道一組對邊平行，可能是梯形。"),
         ("兩條對角線互相垂直", False, "箏形的對角線也互相垂直，不一定是平行四邊形。"),
         ("一組鄰邊相等", False, "箏形也有鄰邊相等，不一定是平行四邊形。")]


def s3(seen):
    out = [mcq("四邊形 ABCD 中「%s」，它一定是平行四邊形嗎？" % c, "一定是" if ok else "不一定", ["不一定" if ok else "一定是", "一定不是", "一定是長方形"], why) for c, ok, why in CONDS]
    for b in out:
        seen.add(b["q"])

    def num_cond():
        a, b = R.randint(4, 15), R.randint(4, 15)
        if a == b:
            return None
        t = R.choice(["ok", "trap"])
        if t == "ok":
            q = "四邊形 ABCD 中，%s ＝ %s ＝ %d，%s ＝ %s ＝ %d，它是平行四邊形嗎？" % (ov("AB"), ov("CD"), a, ov("BC"), ov("AD"), b)
            return mcq(q, "是，兩組對邊分別相等", ["不是，鄰邊不相等", "不一定，要知道角度", "是，因為對角線相等"], "兩組對邊分別相等，所以是平行四邊形。")
        q = "四邊形 ABCD 中，%s // %s，%s ＝ %s ＝ %d，它一定是平行四邊形嗎？" % (ov("AD"), ov("BC"), ov("AB"), ov("CD"), a)
        return mcq(q, "不一定，可能是等腰梯形", ["一定是，一組對邊平行且相等", "一定是，兩組對邊相等", "一定是長方形"], "平行的是 AD、BC，相等的是另一組 AB、CD，可能是等腰梯形。")
    return out + pick_unique(R, num_cond, 10, seen)


def s4(seen):
    def ang_eq():
        x = R.randint(10, 40)
        a, c = R.randint(2, 4), R.randint(-10, 30)
        A = a * x + c
        if not 30 < A < 150 or A == 90:
            return None
        k = R.choice(["opp", "adj"])
        if k == "opp":
            b = R.randint(1, a - 1) if a > 1 else 1
            d = A - b * x
            q = "平行四邊形 ABCD 中，∠A ＝（%dx%s）°，∠C ＝（%sx%s）°，x 是多少？" % (a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else "", "" if b == 1 else b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "")
            return mcq(q, str(x), [str(A), str(x + 5), str((180 - c - d) // (a + b)) if (180 - c - d) % (a + b) == 0 and (180 - c - d) // (a + b) != x else str(x - 2)], "對角相等：列方程式解得 x ＝ %d（∠A ＝ %d°）。" % (x, A))
        B = 180 - A
        b = R.randint(1, 3)
        d = B - b * x
        q = "平行四邊形 ABCD 中，∠A ＝（%dx%s）°，∠B ＝（%sx%s）°，x 是多少？" % (a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else "", "" if b == 1 else b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "")
        wrong = (d - c) // (a - b) if a != b and (d - c) % (a - b) == 0 and (d - c) // (a - b) > 0 and (d - c) // (a - b) != x else x + 4
        return mcq(q, str(x), [str(wrong), str(x + 2), str(A)], "鄰角互補：（%dx%s）＋（%sx%s）＝ 180，x ＝ %d。" % (a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else "", "" if b == 1 else b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "", x))

    def side_eq():
        x = R.randint(2, 9)
        a, c = R.randint(2, 5), R.randint(-3, 6)
        L = a * x + c
        if L <= 0:
            return None
        b = R.randint(1, a - 1)
        d = L - b * x
        q = "平行四邊形 ABCD 中，%s ＝ %dx%s，%s ＝ %sx%s，x 是多少？" % (ov("AB"), a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else "", ov("CD"), "" if b == 1 else b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "")
        return mcq(q, str(x), [str(L), str(x + 1), str(x + 3)], "對邊相等：列方程式得 x ＝ %d（%s ＝ %d）。" % (x, ov("AB"), L))
    return pick_unique(R, ang_eq, 12, seen) + pick_unique(R, side_eq, 8, seen)


def s5(seen):
    def perim():
        a, b = R.randint(4, 25), R.randint(4, 25)
        P = 2 * (a + b)
        q = "平行四邊形的周長是 %d 公分，一邊長 %d 公分，相鄰的另一邊長是多少公分？" % (P, a)
        return mcq(q, "%d 公分" % b, ["%d 公分" % x for x in (P - a, P // 2, (P - 2 * a) if (P - 2 * a) != b else b + 2)], "鄰邊和 ＝ %d ÷ 2 ＝ %d，%d － %d ＝ %d（公分）。" % (P, a + b, a + b, a, b))

    def area4():
        A = R.choice(range(24, 241, 4))
        q = "平行四邊形 ABCD 的面積是 %d 平方公分，對角線交於 O，△AOB 的面積是多少平方公分？" % A
        return mcq(q, "%d 平方公分" % (A // 4), ["%d 平方公分" % x for x in (A // 2, A // 3 if A % 3 == 0 else A // 4 + 2, A // 8 if A % 8 == 0 else A // 4 - 1)], "兩條對角線把平行四邊形分成 4 個面積相等的三角形：%d ÷ 4 ＝ %d。" % (A, A // 4))

    def area_h():
        b, h = R.randint(4, 20), R.randint(3, 15)
        b2 = R.randint(3, 20)
        A = b * h
        if A % b2 or b2 == b:
            return None
        h2 = A // b2
        q = "平行四邊形的兩鄰邊長 %d 公分和 %d 公分，以 %d 公分的邊為底，高是 %d 公分。以 %d 公分的邊為底時，高是多少公分？" % (b, b2, b, h, b2)
        return mcq(q, "%d 公分" % h2, ["%d 公分" % x for x in (h, A, h2 + 1)], "面積 ＝ %d × %d ＝ %d，%d ÷ %d ＝ %d（公分）。" % (b, h, A, A, b2, h2))
    return pick_unique(R, perim, 7, seen) + pick_unique(R, area4, 7, seen) + pick_unique(R, area_h, 6, seen)


def main():
    seen = set()
    sets = [("對邊與對角", s1(seen)), ("對角線", s2(seen)), ("判別平行四邊形", s3(seen)),
            ("列方程式", s4(seen)), ("周長與面積", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["兩組對邊分別平行的四邊形叫<b>平行四邊形</b>。",
         "性質：<b>對邊相等、對角相等、鄰角互補</b>、<b>對角線互相平分</b>；一條對角線分成兩個全等三角形。",
         "判別：兩組對邊相等、兩組對角相等、對角線互相平分、一組對邊平行且相等，都是平行四邊形。"],
        [example("平行四邊形 ABCD，∠A ＝ 70°，求 ∠B、∠C", ["∠B ＝ 180° － 70° ＝ 110°。", "∠C ＝ ∠A。"], "110°、70°"),
         example("對角線交於 O，AC ＝ 18，OA ＝ ？", ["對角線互相平分。"], "9")],
        [("鄰角相等", "鄰角互補，對角才相等"),
         ("平行四邊形的對角線等長", "長方形的對角線才等長"),
         ("一組對邊平行、另一組相等就是平行四邊形", "可能是等腰梯形；要同一組對邊平行且相等")])
    faq = [{"q": "怎麼證明一個四邊形是平行四邊形？",
            "a": "找到下面任何一個就可以：兩組對邊平行、兩組對邊相等、兩組對角相等、對角線互相平分、一組對邊平行且相等。"},
           {"q": "平行四邊形的對角線有什麼性質？",
            "a": "兩條對角線互相平分，交點是對稱中心，把平行四邊形分成 4 個面積相等的三角形；但不一定等長，也不一定垂直。"},
           {"q": "八年級的平行四邊形要學什麼？",
            "a": "108課綱 S-8-9：平行四邊形的基本性質與判別：對邊相等、對角相等、對角線互相平分等。"}]
    make_unit(R, "grade-8", "parallelograms", "S-8-9",
              "平行四邊形的基本性質：關於平行四邊形的內角、邊、對角線等的幾何性質。",
              "平行四邊形的性質與判別",
              "八年級數學 平行四邊形 練習題｜對邊・對角・對角線互相平分 學習單（附解答）",
              "平行四邊形",
              "國中八年級數學「平行四邊形的性質與判別」免費學習單：對邊相等、對角相等、鄰角互補、對角線互相平分、判別平行四邊形、列方程式、周長與面積。100題線上練習馬上對答案，附可列印解答。",
              "對邊相等、對角相等、對角線互相平分",
              "鄰角互補；一組對邊平行且相等就是平行四邊形。",
              body, faq, sets, 23)


if __name__ == "__main__":
    main()
