# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：長方形、菱形、正方形、箏形與梯形（108課綱 S-8-10、S-8-11）
  python3 tools/gen_tw_math_g8_special_quadrilaterals.py
特殊四邊形の性質（對角線の長さ・垂直・平分）、長方形の對角線と角、菱形の邊と面積（對角線の積 ÷ 2）、箏形、等腰梯形の底角、梯形の中線（上底＋下底）÷ 2。
誤答：菱形の對角線が等長とする、面積で ÷ 2 を忘れる、中線を（下底 － 上底）÷ 2 とする、等腰梯形の上下の角の取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets

R = random.Random(81024)
SH = ["長方形", "菱形", "正方形", "箏形", "等腰梯形", "平行四邊形"]
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25), (15, 20, 25), (12, 5, 13), (4, 3, 5), (8, 6, 10), (15, 8, 17)]


def ov(s):
    return "<span class='ov'>%s</span>" % s


PROPS = [
    ("對角線等長且互相平分，但不一定垂直", "長方形", "長方形的對角線等長且互相平分；要再垂直才是正方形。"),
    ("對角線互相垂直平分，但不一定等長", "菱形", "菱形的對角線互相垂直平分；要再等長才是正方形。"),
    ("對角線等長、互相垂直且互相平分", "正方形", "正方形同時是長方形和菱形，對角線等長、垂直、互相平分。"),
    ("兩組鄰邊分別相等，對角線互相垂直，只有一條被另一條平分", "箏形", "箏形有兩組相等的鄰邊，對角線垂直，其中一條被平分。"),
    ("只有一組對邊平行，兩腰相等，對角線等長", "等腰梯形", "等腰梯形兩腰相等、同一底的兩個底角相等、對角線等長。"),
    ("四個角都是直角，但四邊不一定相等", "長方形", "四個直角是長方形；四邊也相等才是正方形。"),
    ("四邊都相等，但角不一定是直角", "菱形", "四邊相等是菱形；角也都是直角才是正方形。"),
    ("四邊相等而且四個角都是直角", "正方形", "四邊相等又四個直角，就是正方形。"),
    ("對邊平行且相等，對角線互相平分，但不一定等長也不一定垂直", "平行四邊形", "一般平行四邊形的對角線只保證互相平分。"),
]


def s1(seen):
    out = [mcq("哪一種四邊形的性質是：%s？" % p, a, [x for x in SH if x != a], e) for p, a, e in PROPS]
    TF = [("正方形是長方形", "對", "正方形四個角都是直角，所以是特殊的長方形。"),
          ("長方形是正方形", "不對", "長方形四邊不一定相等，不一定是正方形。"),
          ("菱形是平行四邊形", "對", "菱形兩組對邊平行，是特殊的平行四邊形。"),
          ("箏形是平行四邊形", "不對", "箏形的對邊不平行，不是平行四邊形。"),
          ("正方形是菱形", "對", "正方形四邊相等，所以是特殊的菱形。"),
          ("菱形的對角線一定等長", "不對", "菱形對角線互相垂直平分，等長時才是正方形。"),
          ("梯形的兩腰一定平行", "不對", "梯形只有一組對邊（上底和下底）平行。"),
          ("等腰梯形的對角線等長", "對", "等腰梯形可用全等三角形證明兩條對角線等長。"),
          ("箏形的對角線互相垂直", "對", "箏形的兩條對角線互相垂直。"),
          ("長方形的對角線互相垂直", "不對", "長方形對角線等長且互相平分，但只有正方形才垂直。"),
          ("菱形的對角線平分它的內角", "對", "菱形的每條對角線都平分它經過的兩個內角。")]
    out += [mcq("「%s」，這句話對嗎？" % s, a, ["不對" if a == "對" else "對", "只有邊長是整數時才對", "不能判斷"], e) for s, a, e in TF]
    for b in out:
        seen.add(b["q"])
    return out


def s2(seen):
    def diag():
        x = R.randint(3, 20)
        q = "長方形 ABCD 的對角線交於 O，%s ＝ %d，%s 是多少？" % (ov("OA"), x, ov("BD"))
        return mcq(q, str(2 * x), [str(x), str(x * x), str(4 * x)], "長方形對角線等長且互相平分：%s ＝ %s ＝ 2 × %d ＝ %d。" % (ov("BD"), ov("AC"), x, 2 * x))

    def ang():
        a = R.randint(20, 70)
        k = R.choice(["OBA", "AOB", "OBC"])
        if k == "OBA":
            v, e = a, "OA ＝ OB，△OAB 是等腰三角形：∠OBA ＝ ∠OAB ＝ %d°。" % a
        elif k == "AOB":
            v, e = 180 - 2 * a, "OA ＝ OB，∠OBA ＝ %d°，∠AOB ＝ 180° － 2 × %d° ＝ %d°。" % (a, a, 180 - 2 * a)
        else:
            v, e = 90 - a, "∠ABC ＝ 90°，∠OBA ＝ ∠OAB ＝ %d°，∠OBC ＝ 90° － %d° ＝ %d°。" % (a, a, 90 - a)
        q = "長方形 ABCD 的對角線交於 O，∠OAB ＝ %d°，∠%s 是多少度？" % (a, k)
        return mcq(q, "%d°" % v, ["%d°" % x for x in {a, 180 - 2 * a, 90 - a, 2 * a, 180 - a} if x != v], e)

    def pyth():
        a, b, c = R.choice(TRIP)
        k = R.randint(1, 3)
        q = "長方形的長 %d 公分、寬 %d 公分，對角線長多少公分？" % (a * k, b * k)
        return mcq(q, "%d 公分" % (c * k), ["%d 公分" % x for x in ((a + b) * k, c * k + 1, (a * k) * (b * k) // 2)], "對角線 ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d。" % (a * k, b * k, c * k))
    return pick_unique(R, diag, 6, seen) + pick_unique(R, ang, 8, seen) + pick_unique(R, pyth, 6, seen)


def s3(seen):
    def side():
        a, b, c = R.choice(TRIP)
        k = R.choice([1, 2])
        d1, d2 = 2 * a * k, 2 * b * k
        q = "菱形的兩條對角線長 %d 公分和 %d 公分，邊長是多少公分？" % (d1, d2)
        return mcq(q, "%d 公分" % (c * k), ["%d 公分" % x for x in ((d1 + d2) // 2, 2 * c * k, (d1 + d2) // 4 if (d1 + d2) % 4 == 0 and (d1 + d2) // 4 != c * k else c * k + 1)], "對角線互相垂直平分，一半是 %d 和 %d：邊長 ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d。" % (a * k, b * k, a * k, b * k, c * k))

    def area():
        d1, d2 = R.randint(4, 24), R.randint(4, 24)
        if d1 * d2 % 2:
            return None
        sh = R.choice(["菱形", "箏形", "正方形"])
        if sh == "正方形":
            d2 = d1
        q = "%s的兩條對角線長 %d 公分和 %d 公分，面積是多少平方公分？" % (sh, d1, d2) if sh != "正方形" else "正方形的對角線長 %d 公分，面積是多少平方公分？" % d1
        A = d1 * d2 // 2
        return mcq(q, "%d 平方公分" % A, ["%d 平方公分" % x for x in (d1 * d2, d1 + d2, A // 2 if A % 2 == 0 else A + 1)], "對角線互相垂直，面積 ＝ 對角線 × 對角線 ÷ 2 ＝ %d × %d ÷ 2 ＝ %d。" % (d1, d2, A))

    def rang():
        a = R.randint(40, 140)
        if a == 90:
            return None
        q = "菱形 ABCD 中，∠A ＝ %d°，對角線 %s 和 ∠B 的夾角 ∠ABD 是多少度？" % (a, ov("BD"))
        v = (180 - a) // 2 if (180 - a) % 2 == 0 else None
        if v is None:
            return None
        return mcq(q, "%d°" % v, ["%d°" % x for x in (180 - a, a // 2 if a % 2 == 0 else a, 90 - v if 90 - v != v else v + 5)], "∠B ＝ 180° － %d° ＝ %d°，對角線平分 ∠B：%d° ÷ 2 ＝ %d°。" % (a, 180 - a, 180 - a, v))
    return pick_unique(R, side, 8, seen) + pick_unique(R, area, 7, seen) + pick_unique(R, rang, 5, seen)


def s4(seen):
    def iso():
        a = R.randint(40, 85)
        k = R.choice(["B", "C", "D"])
        par_ = "%s // %s" % (ov("AD"), ov("BC"))
        if k == "B":
            q = "等腰梯形 ABCD 中，%s，∠C ＝ %d°，∠B 是多少度？" % (par_, a)
            v, e = a, "同一底的兩個底角相等：∠B ＝ ∠C ＝ %d°。" % a
        elif k == "D":
            q = "等腰梯形 ABCD 中，%s，下底的底角 ∠B ＝ %d°，∠D 是多少度？" % (par_, a)
            v, e = 180 - a, "∠C ＝ ∠B ＝ %d°；∠D 和 ∠C 是同側內角（AD // BC），互補：180° － %d° ＝ %d°。" % (a, a, 180 - a)
        else:
            q = "等腰梯形 ABCD 中，%s，上底的底角 ∠A ＝ %d°，∠C 是多少度？" % (par_, 180 - a)
            v, e = a, "∠B ＝ 180° － ∠A ＝ %d°，同一底的底角相等：∠C ＝ ∠B ＝ %d°。" % (a, a)
        return mcq(q, "%d°" % v, ["%d°" % x for x in (a, 180 - a, 90 - a // 2, 2 * a if 2 * a < 180 else a // 2) if x != v], e)

    def kite():
        a, b = R.randint(60, 140), R.randint(30, 110)
        c = 360 - a - 2 * b
        if not 30 <= c <= 150 or a == b:
            return None
        q = "箏形 ABCD 中，%s ＝ %s，%s ＝ %s，∠A ＝ %d°，∠B ＝ %d°，∠C 是多少度？" % (ov("AB"), ov("AD"), ov("CB"), ov("CD"), a, b)
        return mcq(q, "%d°" % c, ["%d°" % x for x in (360 - a - b, 180 - b, a if a != c else c + 10)], "對稱軸 AC 兩側相同：∠D ＝ ∠B ＝ %d°，∠C ＝ 360° － %d° － %d° × 2 ＝ %d°。" % (b, a, b, c))
    return pick_unique(R, iso, 10, seen) + pick_unique(R, kite, 10, seen)


def s5(seen):
    def mid():
        a, b = R.randint(3, 20), R.randint(8, 40)
        if a >= b or (a + b) % 2:
            return None
        q = "梯形的上底 %d 公分、下底 %d 公分，中線長多少公分？" % (a, b)
        m = (a + b) // 2
        return mcq(q, "%d 公分" % m, ["%d 公分" % x for x in (a + b, (b - a) // 2 if (b - a) // 2 != m else m + 1, b - a if b - a != m else m + 2)], "中線 ＝（上底 ＋ 下底）÷ 2 ＝（%d ＋ %d）÷ 2 ＝ %d。" % (a, b, m))

    def mid_rev():
        a, m = R.randint(3, 15), R.randint(8, 25)
        b = 2 * m - a
        if b <= a:
            return None
        q = "梯形的中線長 %d 公分，上底 %d 公分，下底是多少公分？" % (m, a)
        return mcq(q, "%d 公分" % b, ["%d 公分" % x for x in (m - a if m - a > 0 else m + a, m + a, 2 * m)], "（%d ＋ 下底）÷ 2 ＝ %d，下底 ＝ %d － %d ＝ %d。" % (a, m, 2 * m, a, b))

    def area():
        a, b, h = R.randint(3, 15), R.randint(10, 30), R.randint(3, 15)
        if a >= b or (a + b) % 2:
            return None
        m = (a + b) // 2
        q = "梯形的中線長 %d 公分，高 %d 公分，面積是多少平方公分？" % (m, h)
        return mcq(q, "%d 平方公分" % (m * h), ["%d 平方公分" % x for x in (m * h // 2 if m * h % 2 == 0 else m * h + h, 2 * m * h, m + h)], "梯形面積 ＝（上底 ＋ 下底）× 高 ÷ 2 ＝ 中線 × 高 ＝ %d × %d ＝ %d。" % (m, h, m * h))
    return pick_unique(R, mid, 8, seen) + pick_unique(R, mid_rev, 6, seen) + pick_unique(R, area, 6, seen)


def main():
    seen = set()
    sets = [("認識特殊四邊形", s1(seen)), ("長方形", s2(seen)), ("菱形、正方形與箏形", s3(seen)),
            ("等腰梯形與箏形的角", s4(seen)), ("梯形中線", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>長方形</b>：四個直角，對角線等長且互相平分。<b>菱形</b>：四邊相等，對角線互相垂直平分，也平分內角。<b>正方形</b>：兩種性質都有。",
         "<b>箏形</b>：兩組鄰邊分別相等，對角線互相垂直；面積 ＝ 對角線 × 對角線 ÷ 2（菱形、正方形也可以這樣算）。",
         "<b>等腰梯形</b>：兩腰相等，同一底的兩個底角相等，對角線等長。",
         "<b>梯形中線</b>（兩腰中點的連線）平行上下底，長度 ＝（上底 ＋ 下底）÷ 2。"],
        [example("菱形對角線 6 和 8，邊長和面積", ["一半是 3 和 4，邊長 √（9 ＋ 16）＝ 5。", "面積 6 × 8 ÷ 2 ＝ 24。"], "5、24"),
         example("梯形上底 6、下底 14，中線？", ["（6 ＋ 14）÷ 2。"], "10")],
        [("菱形的對角線等長", "菱形對角線互相垂直，等長時才是正方形"),
         ("菱形面積 ＝ 對角線 × 對角線", "還要 ÷ 2"),
         ("中線 ＝（下底 － 上底）÷ 2", "是兩底相加再 ÷ 2")])
    faq = [{"q": "正方形、長方形、菱形是什麼關係？",
            "a": "正方形既是長方形（四個直角）也是菱形（四邊相等）；長方形和菱形又都是平行四邊形。"},
           {"q": "為什麼菱形和箏形的面積是對角線相乘除以 2？",
            "a": "它們的對角線互相垂直，可以把圖形補成一個長方形，長方形的長和寬就是兩條對角線，原圖形剛好是一半。"},
           {"q": "八年級的特殊四邊形要學什麼？",
            "a": "108課綱 S-8-10、S-8-11：正方形、長方形、箏形的基本性質，以及梯形（等腰梯形、梯形中線）的基本性質。"}]
    make_unit(R, "grade-8", "special-quadrilaterals", "S-8-10",
              "正方形、長方形、箏形的基本性質：長方形的對角線等長且互相平分；菱形對角線互相垂直平分；箏形的其中一條對角線垂直平分另一條對角線。",
              "長方形、菱形、正方形、箏形與梯形",
              "八年級數學 特殊四邊形 練習題｜菱形・箏形・等腰梯形・梯形中線 學習單（附解答）",
              "特殊四邊形",
              "國中八年級數學「長方形、菱形、正方形、箏形與梯形」免費學習單：特殊四邊形的對角線性質、長方形的角和對角線、菱形邊長與面積、等腰梯形與箏形的角、梯形中線。100題線上練習馬上對答案，附可列印解答。",
              "梯形中線 ＝（上底 ＋ 下底）÷ 2",
              "菱形、箏形、正方形面積 ＝ 對角線 × 對角線 ÷ 2。",
              body, faq, sets, 24)


if __name__ == "__main__":
    main()
