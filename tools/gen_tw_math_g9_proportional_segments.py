# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：平行線截比例線段（108課綱 S-9-3）
  python3 tools/gen_tw_math_g9_proportional_segments.py
三角形兩邊中點連線（中點連線定理）、DE // BC のとき AD：DB ＝ AE：EC、比例から平行の判定、三本の平行線と二本の截線、應用。
誤答：中點連線を第三邊と同じ長さにする、AD：AB と AD：DB の取り違え、差を等しくすれば平行とする。
"""
import random
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr
from tw_g7 import tidy_sets
from tw_g9 import ov, poly_svg

R = random.Random(81104)


def tri(lab, mid=False):
    pts = {"A": (90, 150), "B": (0, 0), "C": (170, 0), "D": (45 if mid else 36, 75 if mid else 60), "E": (130 if mid else 138, 75 if mid else 60)}
    return poly_svg(pts, [["A", "B", "C", "A"], ["D", "E"]], lab, label="三角形與平行線", lg=True)


def three(lab):
    pts = {"A": (0, 140), "B": (40, 70), "C": (90, -20), "D": (150, 140), "E": (170, 70), "F": (196, -20)}
    ext = ""
    return poly_svg(pts, [["A", "D"], ["B", "E"], ["C", "F"], ["A", "B", "C"], ["D", "E", "F"]], lab, label="三條平行線", lg=True)


def s1(seen):
    def mk():
        bc = R.randint(3, 30) * 2
        k = R.choice(["DE", "BC", "P"])
        if k == "DE":
            q = "D、E 分別是 %s、%s 的中點，%s ＝ %d，%s 是多少？" % (ov("AB"), ov("AC"), ov("BC"), bc, ov("DE"))
            return mcq(q, str(bc // 2), [str(bc), str(bc * 2), str(bc // 2 + 1)], "中點連線平行第三邊，長度是第三邊的一半：%d ÷ 2 ＝ %d。" % (bc, bc // 2))
        if k == "BC":
            q = "D、E 分別是 %s、%s 的中點，%s ＝ %d，%s 是多少？" % (ov("AB"), ov("AC"), ov("DE"), bc // 2, ov("BC"))
            return mcq(q, str(bc), [str(bc // 2), str(bc // 4) if bc % 4 == 0 else str(bc + 1), str(bc * 2)], "%s ＝ 2 × %s ＝ 2 × %d ＝ %d。" % (ov("BC"), ov("DE"), bc // 2, bc))
        a, b, c = R.randint(4, 20) * 2, R.randint(4, 20) * 2, R.randint(4, 20) * 2
        if max(a, b, c) * 2 >= a + b + c:
            return None
        q = "△ABC 三邊長 %d、%d、%d，連接三邊中點得到的三角形周長是多少？" % (a, b, c)
        P = (a + b + c) // 2
        return mcq(q, str(P), [str(a + b + c), str(P // 2) if P % 2 == 0 else str(P + 1), str(P + 3)], "三條中點連線各是對應邊的一半，周長是原來的一半：%d ÷ 2 ＝ %d。" % (a + b + c, P))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 6), R.randint(1, 6)
        if gcd(a, b) > 1:
            return None
        k1, k2 = R.randint(1, 4), R.randint(1, 4)
        AD, DB, AE, EC = a * k1, b * k1, a * k2, b * k2
        hide = R.choice(["DB", "AE", "EC"])
        val = {"DB": DB, "AE": AE, "EC": EC}[hide]
        lab = {("A", "D"): str(AD), ("D", "B"): str(DB), ("A", "E"): str(AE), ("E", "C"): str(EC)}
        key = {"DB": ("D", "B"), "AE": ("A", "E"), "EC": ("E", "C")}[hide]
        lab[key] = "x"
        q = "%s // %s，求 x。（圖形不一定按比例）" % (ov("DE"), ov("BC")) + tri(lab)
        wrong = [AD + DB, AE + EC, val + 1, abs(AE - AD) + DB if abs(AE - AD) + DB != val else val + 2]
        return mcq(q, str(val), [str(w) for w in wrong if w != val], "平行線截比例線段：%s：%s ＝ %s：%s，%d：%d ＝ %d：%d，x ＝ %d。" % (ov("AD"), ov("DB"), ov("AE"), ov("EC"), AD, DB, AE, EC, val))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(1, 6), R.randint(1, 6)
        k1 = R.randint(1, 4)
        ok = R.random() < .5
        AD, DB = a * k1, b * k1
        if ok:
            k2 = R.randint(1, 4)
            AE, EC = a * k2, b * k2
        else:
            AE, EC = a * k1 + 1, b * k1 + 1
        if (AD * EC == DB * AE) != ok:
            return None
        q = "△ABC 中，D 在 %s 上，E 在 %s 上，%s ＝ %d、%s ＝ %d、%s ＝ %d、%s ＝ %d。%s 和 %s 平行嗎？" % (ov("AB"), ov("AC"), ov("AD"), AD, ov("DB"), DB, ov("AE"), AE, ov("EC"), EC, ov("DE"), ov("BC"))
        ans = "平行" if ok else "不平行"
        return mcq(q, ans, ["不平行" if ok else "平行", "互相垂直", "無法判斷"], "%d：%d %s %d：%d，%s，所以%s。" % (AD, DB, "＝" if ok else "≠", AE, EC, "線段成比例" if ok else "不成比例", ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        k = R.randint(2, 4)
        if a == b:
            return None
        AB, BC, DE, EF = a, b, a * k, b * k
        hide = R.choice(["BC", "DE", "EF"])
        val = {"BC": BC, "DE": DE, "EF": EF}[hide]
        lab = {("A", "B"): str(AB), ("B", "C"): str(BC), ("D", "E"): str(DE), ("E", "F"): str(EF)}
        lab[{"BC": ("B", "C"), "DE": ("D", "E"), "EF": ("E", "F")}[hide]] = "x"
        q = "三條平行線 %s // %s // %s 截兩條直線，求 x。（圖形不一定按比例）" % (ov("AD"), ov("BE"), ov("CF")) + three(lab)
        return mcq(q, str(val), [str(w) for w in (val + 1, AB + BC + DE + EF - val * 3 if AB + BC + DE + EF - val * 3 > 0 else val + 3, val * 2) if w != val], "平行線截比例線段：%s：%s ＝ %s：%s，%d：%d ＝ %d：%d，x ＝ %d。" % (ov("AB"), ov("BC"), ov("DE"), ov("EF"), AB, BC, DE, EF, val))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def ladder():
        n = R.choice([3, 4, 5])
        top, bot = R.randint(20, 40), R.randint(50, 80)
        if (bot - top) % n:
            return None
        d = (bot - top) // n
        k = R.randint(1, n - 1)
        q = "一個上窄下寬的梯子有 %d 根等距的平行橫木，最上面長 %d 公分，最下面長 %d 公分，由上往下第 %d 根長多少公分？" % (n + 1, top, bot, k + 1)
        v = top + k * d
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in ((top + bot) // 2 if (top + bot) // 2 != v else v + d, v + d, top + k * (bot - top) // (n + 1))] , "等距的平行橫木把兩側柱分成相等的段，長度每根增加（%d － %d）÷ %d ＝ %d 公分：%d ＋ %d × %d ＝ %d。" % (bot, top, n, d, top, k, d, v))

    def mid_trap():
        a, b = R.randint(4, 20), R.randint(10, 40)
        if a >= b or (a + b) % 2:
            return None
        q = "梯形 ABCD 中 %s // %s，E、F 分別是兩腰的中點，%s ＝ %d，%s ＝ %d，%s 是多少？" % (ov("AD"), ov("BC"), ov("AD"), a, ov("BC"), b, ov("EF"))
        v = (a + b) // 2
        return mcq(q, str(v), [str(a + b), str((b - a) // 2) if (b - a) // 2 != v else str(v + 1), str(b // 2) if b // 2 != v else str(v + 2)], "連對角線用兩次中點連線定理：%s ＝（%d ＋ %d）÷ 2 ＝ %d。" % (ov("EF"), a, b, v))

    def road():
        a, b = R.randint(2, 6), R.randint(2, 6)
        k = R.randint(10, 40)
        if a == b:
            return None
        q = "三條互相平行的街道被兩條路所截。第一條路上，街道之間的距離是 %d 公尺和 %d 公尺；第二條路上，第一段長 %d 公尺，第二段長多少公尺？" % (a * 10, b * 10, a * k)
        v = b * k
        return mcq(q, "%d 公尺" % v, ["%d 公尺" % x for x in (b * 10 + a * k - a * 10, a * k, v + k)], "平行線截比例線段：%d：%d ＝ %d：x，x ＝ %d。" % (a * 10, b * 10, a * k, v))
    return pick_unique(R, ladder, 6, seen) + pick_unique(R, mid_trap, 8, seen) + pick_unique(R, road, 6, seen)


def main():
    seen = set()
    sets = [("三角形的中點連線", s1(seen)), ("平行線截三角形兩邊", s2(seen)), ("判別兩線平行", s3(seen)),
            ("三條平行線截兩直線", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>中點連線定理</b>：三角形兩邊中點的連線平行第三邊，長度是第三邊的一半。",
         "<b>平行線截比例線段</b>：%s // %s 時，%s：%s ＝ %s：%s。三條平行線截兩條直線，截出的線段也成比例。" % (ov("DE"), ov("BC"), ov("AD"), ov("DB"), ov("AE"), ov("EC")),
         "反過來，%s：%s ＝ %s：%s 時，%s // %s。" % (ov("AD"), ov("DB"), ov("AE"), ov("EC"), ov("DE"), ov("BC")) + tri({("A", "D"): "3", ("D", "B"): "2", ("A", "E"): "6", ("E", "C"): "x"})],
        [example("上圖 %s // %s，求 x" % (ov("DE"), ov("BC")), ["3：2 ＝ 6：x。"], "x ＝ 4"),
         example("D、E 是 AB、AC 的中點，BC ＝ 18，DE？", ["DE 是 BC 的一半。"], "9")],
        [("中點連線和第三邊一樣長", "只有一半"),
         ("%s：%s ＝ %s：%s 就說線段差相同也平行" % (ov("AD"), ov("DB"), ov("AE"), ov("EC")), "要比例相同，不是差相同"),
         ("把 %s：%s 寫成 %s：%s" % (ov("AD"), ov("DB"), ov("DE"), ov("BC")), "DE：BC 要用 AD：AB")])
    faq = [{"q": "平行線截比例線段和相似三角形有什麼關係？",
            "a": "DE // BC 時 △ADE ～ △ABC，由相似可推出 AD：AB ＝ AE：AC，再推出 AD：DB ＝ AE：EC。"},
           {"q": "梯形中線為什麼是上下底和的一半？",
            "a": "連一條對角線，把梯形分成兩個三角形，各用一次中點連線定理，兩段加起來就是（上底 ＋ 下底）÷ 2。"},
           {"q": "九年級的平行線截比例線段要學什麼？",
            "a": "108課綱 S-9-3：三角形兩邊中點連線平行第三邊且等於一半、平行線截比例線段性質、用截線段成比例判定平行，以及應用。"}]
    make_unit(R, "grade-9", "proportional-segments", "S-9-3",
              "平行線截比例線段：連接三角形兩邊中點的線段必平行於第三邊（其長度等於第三邊的一半）；平行線截比例線段性質；利用截線段成比例判定兩直線平行；平行線截比例線段性質的應用。",
              "平行線截比例線段與中點連線",
              "九年級數學 平行線截比例線段 練習題｜中點連線定理 學習單（附解答）",
              "平行線截比例線段",
              "國中九年級數學「平行線截比例線段與中點連線」免費學習單：三角形中點連線定理、平行線截三角形兩邊成比例、判別兩線平行、三條平行線截兩直線、梯子和梯形中線應用題。100題線上練習馬上對答案，附可列印解答。",
              "%s // %s ⇒ %s：%s ＝ %s：%s" % (ov("DE"), ov("BC"), ov("AD"), ov("DB"), ov("AE"), ov("EC")),
              "中點連線平行第三邊，長度是第三邊的一半。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
