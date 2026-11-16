# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：三角形的基本性質（108課綱 S-8-8）
  python3 tools/gen_tw_math_g8_triangle_properties.py
等腰三角形の底角、大角對大邊・大邊對大角、兩邊和大於第三邊（三角形ができるか・第三邊の範圍）、外角＝不相鄰兩內角の和、まとめ。
誤答：頂角と底角の取り違え、等號を含めて三角形ができるとする、第三邊の範圍で差を落とす、大きい角の向かいの邊を取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets

R = random.Random(81021)


def ov(s):
    return "<span class='ov'>%s</span>" % s


def s1(seen):
    def base():
        top = R.randrange(20, 161, 2)
        b = (180 - top) // 2
        q = "等腰三角形的頂角是 %d°，每一個底角是多少度？" % top
        return mcq(q, "%d°" % b, ["%d°" % v for v in (180 - top, top, 90 - top // 2 if 90 - top // 2 != b else b + 10, b + 5)], "兩個底角相等：（180° － %d°）÷ 2 ＝ %d°。" % (top, b))

    def top_():
        b = R.randint(20, 85)
        t = 180 - 2 * b
        q = "等腰三角形的一個底角是 %d°，頂角是多少度？" % b
        return mcq(q, "%d°" % t, ["%d°" % v for v in (180 - b, b, 90 - b if 90 - b != t else t + 10, t + 5)], "兩個底角都是 %d°：180° － %d° × 2 ＝ %d°。" % (b, b, t))

    def amb():
        a = R.choice([40, 50, 70, 80, 30, 20])
        q = "等腰三角形有一個角是 %d°，另外兩個角可能是？" % a
        b = (180 - a) // 2
        ans = "%d°、%d° 或 %d°、%d°" % (b, b, a, 180 - 2 * a)
        return mcq(q, ans, ["只有 %d°、%d°" % (b, b), "只有 %d°、%d°" % (a, 180 - 2 * a), "%d°、%d°" % (a, a)], "%d° 可能是頂角（底角 %d°、%d°），也可能是底角（另一底角 %d°，頂角 %d°）。" % (a, b, b, a, 180 - 2 * a))
    return pick_unique(R, base, 8, seen) + pick_unique(R, top_, 8, seen) + pick_unique(R, amb, 4, seen)


def s2(seen):
    def big_side():
        x, y = R.randint(30, 90), R.randint(20, 80)
        z = 180 - x - y
        if z < 15 or len({x, y, z}) < 3:
            return None
        angs = {"A": x, "B": y, "C": z}
        opp = {"A": ov("BC"), "B": ov("AC"), "C": ov("AB")}
        mx = max(angs, key=angs.get)
        mn = min(angs, key=angs.get)
        k = R.choice(["max", "min"])
        t = mx if k == "max" else mn
        q = "△ABC 中，∠A ＝ %d°，∠B ＝ %d°，哪一邊%s？" % (x, y, "最長" if k == "max" else "最短")
        return mcq(q, opp[t], [opp[v] for v in "ABC" if v != t] + ["三邊一樣長"], "∠C ＝ %d°。%s角對%s邊：∠%s 最%s，它的對邊 %s 最%s。" % (z, "大" if k == "max" else "小", "大" if k == "max" else "小", t, "大" if k == "max" else "小", opp[t], "長" if k == "max" else "短"))

    def big_ang():
        a, b, c = sorted(R.sample(range(4, 16), 3))
        if a + b <= c:
            return None
        sides = {ov("AB"): c, ov("BC"): a, ov("AC"): b}
        R_ = list(sides.items())
        R.shuffle(R_)
        given = "、".join("%s ＝ %d" % kv for kv in R_)
        q = "△ABC 中，%s，哪一個角最大？" % given
        return mcq(q, "∠C", ["∠A", "∠B", "三個角一樣大"], "大邊對大角：最長的邊是 %s ＝ %d，它的對角 ∠C 最大。" % (ov("AB"), c))
    return pick_unique(R, big_side, 12, seen) + pick_unique(R, big_ang, 8, seen)


def s3(seen):
    def can():
        L = sorted([R.randint(2, 15) for _ in range(3)])
        ok = L[0] + L[1] > L[2]
        q = "三根木棒長 %d、%d、%d 公分，能不能圍成一個三角形？" % tuple(R.sample(L, 3))
        ans = "可以" if ok else "不能"
        rs = "%d ＋ %d ＝ %d %s %d" % (L[0], L[1], L[0] + L[1], "＞" if ok else ("＝" if L[0] + L[1] == L[2] else "＜"), L[2])
        return mcq(q, ans, ["不能" if ok else "可以", "只能圍成直角三角形", "要看木棒的粗細"], "兩短邊的和要大於最長邊：%s，所以%s。" % (rs, ans))

    def rng():
        a, b = R.randint(3, 15), R.randint(3, 15)
        if a == b:
            return None
        lo, hi = abs(a - b), a + b
        q = "三角形的兩邊長是 %d 和 %d，第三邊 x 的範圍是？" % (a, b)
        return mcq(q, "%d ＜ x ＜ %d" % (lo, hi), ["%d ≦ x ≦ %d" % (lo, hi), "0 ＜ x ＜ %d" % hi, "x ＞ %d" % lo, "%d ＜ x ＜ %d" % (min(a, b), hi)], "兩邊差 ＜ 第三邊 ＜ 兩邊和：%d － %d ＜ x ＜ %d ＋ %d。" % (max(a, b), min(a, b), a, b))

    def cnt():
        a, b = R.randint(3, 12), R.randint(3, 12)
        if a == b:
            return None
        lo, hi = abs(a - b), a + b
        n = hi - lo - 1
        q = "三角形的兩邊長是 %d 和 %d 公分，第三邊是整數公分，有幾種可能？" % (a, b)
        return mcq(q, "%d 種" % n, ["%d 種" % v for v in (n + 2, n + 1, hi - 1)], "%d ＜ x ＜ %d，整數 x 從 %d 到 %d，共 %d 種。" % (lo, hi, lo + 1, hi - 1, n))
    return pick_unique(R, can, 8, seen) + pick_unique(R, rng, 7, seen) + pick_unique(R, cnt, 5, seen)


def s4(seen):
    def ext():
        a, b = R.randint(25, 80), R.randint(25, 80)
        if a + b > 160:
            return None
        k = R.choice(["ext", "in"])
        if k == "ext":
            q = "△ABC 中，∠A ＝ %d°，∠B ＝ %d°，延長 %s，∠ACD（∠C 的外角）是多少度？" % (a, b, ov("BC") + " 到 D")
            return mcq(q, "%d°" % (a + b), ["%d°" % v for v in (180 - a - b, abs(a - b) if a != b else a + 15, 360 - a - b)], "外角等於不相鄰兩內角的和：%d° ＋ %d° ＝ %d°。" % (a, b, a + b))
        q = "△ABC 中，∠C 的外角是 %d°，∠A ＝ %d°，∠B 是多少度？" % (a + b, a)
        return mcq(q, "%d°" % b, ["%d°" % v for v in (180 - a - b, 180 - b if 180 - b != a + b else b + 10, a + b - 90 if a + b > 90 and a + b - 90 != b else b + 5)], "外角 ＝ ∠A ＋ ∠B：%d° － %d° ＝ %d°。" % (a + b, a, b))
    return pick_unique(R, ext, 20, seen)


def s5(seen):
    def iso_ext():
        b = R.randint(25, 75)
        q = "等腰三角形 ABC 中，%s ＝ %s，∠B ＝ %d°，頂角 ∠A 的外角是多少度？" % (ov("AB"), ov("AC"), b)
        return mcq(q, "%d°" % (2 * b), ["%d°" % v for v in (180 - 2 * b, b, 180 - b)], "∠C ＝ ∠B ＝ %d°，∠A 的外角 ＝ ∠B ＋ ∠C ＝ %d°。" % (b, 2 * b))

    def iso_side():
        a = R.randint(3, 12)
        b = R.randint(3, 12)
        if a == b:
            return None
        # 等腰三角形兩邊長 a、b，可能周長
        opts = []
        if 2 * a > b:
            opts.append(2 * a + b)
        if 2 * b > a:
            opts.append(2 * b + a)
        if len(opts) != 1:
            return None
        P = opts[0]
        q = "等腰三角形的兩邊長是 %d 公分和 %d 公分，周長是多少公分？" % (a, b)
        other = 2 * a + b if P != 2 * a + b else 2 * b + a
        lo = min(a, b)
        return mcq(q, "%d 公分" % P, ["%d 公分" % other, "%d 或 %d 公分" % (min(P, other), max(P, other)), "%d 公分" % (a + b)], "腰是 %d 時 %d ＋ %d ≦ %d 圍不成三角形，所以腰是 %d：周長 %d 公分。" % (lo, lo, lo, max(a, b), max(a, b), P))

    def equi():
        a = R.randint(3, 20)
        q = "正三角形的周長是 %d 公分，每一個角是幾度、邊長是多少？" % (3 * a)
        return mcq(q, "60°，%d 公分" % a, ["90°，%d 公分" % a, "60°，%d 公分" % (3 * a // 2 if 3 * a // 2 != a else a + 1), "180°，%d 公分" % a], "正三角形三邊相等、三角都是 180° ÷ 3 ＝ 60°，邊長 %d ÷ 3 ＝ %d。" % (3 * a, a))
    return pick_unique(R, iso_ext, 7, seen) + pick_unique(R, iso_side, 7, seen) + pick_unique(R, equi, 6, seen)


def main():
    seen = set()
    sets = [("等腰三角形的角", s1(seen)), ("大邊對大角", s2(seen)), ("兩邊和大於第三邊", s3(seen)),
            ("外角性質", s4(seen)), ("綜合", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>等腰三角形兩底角相等</b>，頂角 ＋ 2 × 底角 ＝ 180°。正三角形三個角都是 60°。",
         "<b>大邊對大角、大角對大邊</b>：最長邊的對角最大，最大角的對邊最長。",
         "<b>任意兩邊的和大於第三邊</b>（兩邊的差小於第三邊），否則圍不成三角形。",
         "<b>外角等於不相鄰兩個內角的和</b>。"],
        [example("兩邊長 4、9，第三邊 x 的範圍？", ["9 － 4 ＜ x ＜ 9 ＋ 4。"], "5 ＜ x ＜ 13"),
         example("等腰三角形一個角是 40°，其他兩角？", ["40° 是頂角：70°、70°。", "40° 是底角：40°、100°。"], "70°、70° 或 40°、100°")],
        [("3、4、7 可以圍成三角形", "3 ＋ 4 ＝ 7，不大於 7，圍不成"),
         ("第三邊範圍寫 5 ≦ x ≦ 13", "不能等於，要用 ＜"),
         ("等腰三角形的 40° 一定是頂角", "也可能是底角，兩種都要想")])
    faq = [{"q": "為什麼兩邊和一定要大於第三邊？",
            "a": "兩點之間直線最短，從一個頂點走另外兩邊到另一頂點，一定比直接走那一邊長；等於時三點在同一直線上，圍不成三角形。"},
           {"q": "大邊對大角怎麼用？",
            "a": "比較三角形的邊長就能比較角的大小，反過來也一樣，例如 ∠A 最大，∠A 的對邊 BC 就最長。"},
           {"q": "八年級的三角形性質要學什麼？",
            "a": "108課綱 S-8-8：等腰三角形兩底角相等、大邊對大角、兩邊和大於第三邊、外角等於其內對角和。"}]
    make_unit(R, "grade-8", "triangle-properties", "S-8-8",
              "三角形的基本性質：等腰三角形兩底角相等；非等腰三角形大角對大邊，大邊對大角；三角形兩邊和大於第三邊；外角等於其內對角和。",
              "三角形的基本性質",
              "八年級數學 三角形性質 練習題｜等腰三角形・大邊對大角・兩邊和大於第三邊 學習單（附解答）",
              "三角形性質",
              "國中八年級數學「三角形的基本性質」免費學習單：等腰三角形的底角和頂角、大邊對大角、兩邊和大於第三邊與第三邊範圍、外角性質和綜合題。100題線上練習馬上對答案，附可列印解答。",
              "兩邊和 ＞ 第三邊，大邊對大角",
              "等腰三角形兩底角相等；外角 ＝ 不相鄰兩內角和。",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
