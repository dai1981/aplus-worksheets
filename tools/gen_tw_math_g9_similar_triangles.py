# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：三角形的相似性質（108課綱 S-9-2）
  python3 tools/gen_tw_math_g9_similar_triangles.py
AA・SAS・SSS 相似の判定、△ADE ～ △ABC（DE // BC）で邊を求める、對應の順序、對應高の比・面積比＝相似比の平方、影・鏡・川幅の應用。
誤答：DE：BC を AD：DB にする、面積比を相似比のまま、SSA で相似とする。
"""
import random
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, num, fr
from tw_g7 import tidy_sets
from tw_g9 import ov, poly_svg

R = random.Random(81103)


def ade(lab):
    pts = {"A": (90, 150), "B": (0, 0), "C": (170, 0), "D": (36, 60), "E": (138, 60)}
    return poly_svg(pts, [["A", "B", "C", "A"], ["D", "E"]], lab, label="DE 平行 BC", lg=True)


def s1(seen):
    def mk():
        t = R.choice(["AA", "SAS", "SSS", "SSA", "SSS0"])
        if t == "AA":
            a, b = R.randint(30, 80), R.randint(30, 80)
            q = "△ABC 中 ∠A ＝ %d°、∠B ＝ %d°；△DEF 中 ∠D ＝ %d°、∠F ＝ %d°。兩個三角形相似嗎？" % (a, b, a, 180 - a - b)
            ans, e = "相似（AA）", "∠E ＝ 180° － %d° － %d° ＝ %d° ＝ ∠B，兩組角相等，AA 相似。" % (a, 180 - a - b, b)
        elif t == "SAS":
            p, k = R.randint(2, 9), R.choice([2, 3])
            r_ = R.randint(2, 9)
            g = R.randint(30, 120)
            q = "%s ＝ %d、%s ＝ %d、∠B ＝ %d°；%s ＝ %d、%s ＝ %d、∠E ＝ %d°。△ABC 和 △DEF 相似嗎？" % (ov("AB"), p, ov("BC"), r_, g, ov("DE"), p * k, ov("EF"), r_ * k, g)
            ans, e = "相似（SAS）", "%d：%d ＝ %d：%d，夾角 ∠B ＝ ∠E，SAS 相似。" % (p, p * k, r_, r_ * k)
        elif t == "SSS":
            L = sorted(R.sample(range(3, 12), 3))
            if L[0] + L[1] <= L[2]:
                return None
            k = R.choice([2, 3])
            q = "△ABC 三邊長 %d、%d、%d，△DEF 三邊長 %d、%d、%d。兩個三角形相似嗎？" % tuple(L + [x * k for x in L[::-1]])
            ans, e = "相似（SSS）", "由小到大排：%d：%d ＝ %d：%d ＝ %d：%d ＝ 1：%d，SSS 相似。" % (L[0], L[0] * k, L[1], L[1] * k, L[2], L[2] * k, k)
        elif t == "SSS0":
            L = sorted(R.sample(range(3, 12), 3))
            if L[0] + L[1] <= L[2]:
                return None
            M = [L[0] * 2, L[1] * 2, L[2] * 2 + 1]
            q = "△ABC 三邊長 %d、%d、%d，△DEF 三邊長 %d、%d、%d。兩個三角形相似嗎？" % tuple(L + M)
            ans, e = "不相似", "%d：%d ＝ 1：2，但 %d：%d ≠ 1：2，三邊不成比例。" % (L[0], M[0], L[2], M[2])
        else:
            p, r_ = R.randint(3, 9), R.randint(3, 9)
            g = R.randint(30, 80)
            q = "%s ＝ %d、%s ＝ %d、∠C ＝ %d°；%s ＝ %d、%s ＝ %d、∠F ＝ %d°。由這些條件能確定 △ABC ～ △DEF 嗎？" % (ov("AB"), p, ov("BC"), r_, g, ov("DE"), 2 * p, ov("EF"), 2 * r_, g)
            ans, e = "不一定相似", "相等的角 ∠C 不是 AB、BC 的夾角（SSA），不能確定相似。"
        return mcq(q, ans, [x for x in ["相似（AA）", "相似（SAS）", "相似（SSS）", "不相似", "不一定相似"] if x != ans][:3] if ans not in ("不相似", "不一定相似") else ["相似（AA）", "相似（SAS）", "相似（SSS）"], e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(1, 9)
        if gcd(a, b) > 1 and R.random() < .5:
            return None
        k = R.randint(1, 3)
        AD, DB = a * k, b * k
        de = a * R.randint(1, 3)
        bc = de * (a + b) // a
        if de * (a + b) % a:
            return None
        t = R.choice(["BC", "DE", "DB"])
        if t == "BC":
            lab = {("A", "D"): str(AD), ("D", "B"): str(DB), ("D", "E"): str(de), ("B", "C"): "x"}
            v, w = bc, [de * DB // AD if de * DB % AD == 0 and de * DB // AD != bc else bc + 1, de + DB, de * 2 if de * 2 != bc else bc + 2]
            e = "△ADE ～ △ABC（AA），%s：%s ＝ %s：%s，%d：%d ＝ %d：x，x ＝ %d。" % (ov("AD"), ov("AB"), ov("DE"), ov("BC"), AD, AD + DB, de, bc)
        elif t == "DE":
            lab = {("A", "D"): str(AD), ("D", "B"): str(DB), ("D", "E"): "x", ("B", "C"): str(bc)}
            v, w = de, [bc * AD // DB if bc * AD % DB == 0 and bc * AD // DB != de else de + 1, bc - DB if bc - DB > 0 and bc - DB != de else de + 2, bc // 2 if bc % 2 == 0 and bc // 2 != de else de + 3]
            e = "%s：%s ＝ %s：%s，%d：%d ＝ x：%d，x ＝ %d。" % (ov("AD"), ov("AB"), ov("DE"), ov("BC"), AD, AD + DB, bc, de)
        else:
            lab = {("A", "D"): str(AD), ("D", "B"): "x", ("D", "E"): str(de), ("B", "C"): str(bc)}
            v, w = DB, [AD + DB, AD * bc // de - AD + 1, DB + 2]
            e = "%s：%s ＝ %s：%s，%d：AB ＝ %d：%d，AB ＝ %d，x ＝ %d － %d ＝ %d。" % (ov("AD"), ov("AB"), ov("DE"), ov("BC"), AD, de, bc, AD + DB, AD + DB, AD, DB)
        q = "%s // %s，求 x。（圖形不一定按比例）" % (ov("DE"), ov("BC")) + ade(lab)
        return mcq(q, str(v), [str(x) for x in w if x != v and x > 0] + [str(v + 4)], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        L = sorted(R.sample(range(3, 15), 3))
        if L[0] + L[1] <= L[2]:
            return None
        k = R.choice([2, 3])
        names = R.choice(["DEF", "PQR"])
        perm = list(range(3))
        R.shuffle(perm)
        tgt = "".join(names[i] for i in perm)
        S = {"AB": L[0], "BC": L[1], "CA": L[2]}
        q = "△ABC ～ △%s，%s ＝ %d、%s ＝ %d、%s ＝ %d，相似比是 1：%d。%s%s 是多少？" % (tgt, ov("AB"), L[0], ov("BC"), L[1], ov("CA"), L[2], k, "", ov(tgt[1] + tgt[2]))
        v = L[1] * k
        return mcq(q, str(v), [str(L[0] * k), str(L[2] * k), str(L[1] + k)], "按頂點順序：%s 對應 %s，%d × %d ＝ %d。" % (ov(tgt[1] + tgt[2]), ov("BC"), L[1], k, v))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def area():
        a, b = R.randint(1, 5), R.randint(2, 7)
        if a >= b or gcd(a, b) > 1:
            return None
        A = a * a * R.randint(2, 9)
        q = "△ABC ～ △DEF，相似比是 %d：%d，△ABC 的面積是 %d 平方公分，△DEF 的面積是多少平方公分？" % (a, b, A)
        v = A // (a * a) * b * b
        return mcq(q, "%d 平方公分" % v, ["%d 平方公分" % x for x in (A * b // a if A * b % a == 0 and A * b // a != v else v + 1, A + b - a, v * 2)], "面積比 ＝ 相似比的平方 ＝ %d：%d，%d ÷ %d × %d ＝ %d。" % (a * a, b * b, A, a * a, b * b, v))

    def ratio_from_area():
        a, b = R.randint(1, 6), R.randint(2, 9)
        if a >= b or gcd(a, b) > 1:
            return None
        q = "兩個相似三角形的面積比是 %d：%d，它們的相似比是多少？" % (a * a, b * b)
        return mcq(q, "%d：%d" % (a, b), ["%d：%d" % (a * a, b * b), "%d：%d" % (a * a * a, b * b * b) if a > 1 else "1：%d" % (2 * b), "%d：%d" % (b, a)], "相似比的平方 ＝ 面積比，√%d：√%d ＝ %d：%d。" % (a * a, b * b, a, b))

    def height():
        a, b = R.randint(2, 6), R.randint(3, 9)
        if a >= b:
            return None
        h = a * R.randint(1, 4)
        q = "△ABC ～ △DEF，%s ＝ %d，%s ＝ %d，△ABC 中 BC 邊上的高是 %d，△DEF 中 EF 邊上的高是多少？" % (ov("BC"), a * 2, ov("EF"), b * 2, h)
        v = h * b // a if h * b % a == 0 else None
        if v is None:
            return None
        return mcq(q, str(v), [str(h * b * b // (a * a)) if h * b * b % (a * a) == 0 and h * b * b // (a * a) != v else str(v + 1), str(h + 2 * (b - a)), str(h * 2)], "對應高的比 ＝ 相似比 ＝ %d：%d，%d × %d ÷ %d ＝ %d。" % (a, b, h, b, a, v))
    return pick_unique(R, area, 8, seen) + pick_unique(R, ratio_from_area, 6, seen) + pick_unique(R, height, 6, seen)


def s5(seen):
    def shadow():
        p = R.choice([150, 160, 170, 180])
        ps = R.choice([50, 60, 80, 90, 100, 120])
        ts = R.randint(4, 20) * 100
        h = p * ts // ps
        if p * ts % ps or h % 100 or h > 2000:
            return None
        q = "同一時間，身高 %d 公分的人影子長 %d 公分，一棵樹的影子長 %s 公尺，樹高多少公尺？" % (p, ps, num(ts // 100))
        v = h // 100
        return mcq(q, "%d 公尺" % v, ["%d 公尺" % x for x in (ts * ps // p // 100 if ts * ps // p // 100 not in (v, 0) else v + 1, ts // 100 + (p - ps) // 100 + 1, v * 2)], "陽光平行，人和影子、樹和影子形成相似三角形：%d：%d ＝ 樹高：%s，樹高 ＝ %s 公分 ＝ %d 公尺。" % (p, ps, num(ts), num(h), v))

    def mirror():
        e = R.choice([150, 160])
        d1 = R.choice([2, 3, 4])
        d2 = d1 * R.randint(3, 8)
        H = e * d2 // d1
        q = "把鏡子平放在地上，人站在離鏡子 %d 公尺處，眼睛高 %d 公分，剛好從鏡中看到大樓頂端。鏡子離大樓 %d 公尺，大樓高多少公尺？" % (d1, e, d2)
        v = H / 100
        vs = ("%g" % v)
        return mcq(q, "%s 公尺" % vs, ["%g 公尺" % x for x in (e * d1 / d2 / 100, d2 + e / 100, v * 2)], "入射角 ＝ 反射角，兩個直角三角形相似：%d：%d ＝ %d：%d，大樓高 %s 公分 ＝ %s 公尺。" % (e, d1, H, d2, num(H), vs))

    def river():
        a, b = R.randint(2, 6), R.randint(3, 10)
        k = R.randint(3, 10)
        q = "用兩個相似三角形測河寬：小三角形的一邊 %d 公尺，對應大三角形的邊是 %d 公尺；小三角形中對應河寬的邊是 %d 公尺。河寬是多少公尺？" % (a, a * k, b)
        v = b * k
        return mcq(q, "%d 公尺" % v, ["%d 公尺" % x for x in (b + a * k - a, a * k, b * a)], "相似比 %d：%d ＝ 1：%d，河寬 ＝ %d × %d ＝ %d 公尺。" % (a, a * k, k, b, k, v))
    return pick_unique(R, shadow, 8, seen) + pick_unique(R, mirror, 6, seen) + pick_unique(R, river, 6, seen)


def main():
    seen = set()
    sets = [("判斷相似", s1(seen)), ("平行線與相似三角形", s2(seen)), ("對應邊", s3(seen)),
            ("面積比與高的比", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["三角形相似的判別：<b>AA</b>（兩角相等）、<b>SAS</b>（兩邊成比例且夾角相等）、<b>SSS</b>（三邊成比例）。",
         "%s // %s 時，△ADE ～ △ABC：%s：%s ＝ %s：%s ＝ %s：%s。" % (ov("DE"), ov("BC"), ov("AD"), ov("AB"), ov("AE"), ov("AC"), ov("DE"), ov("BC")),
         "相似三角形：對應高的比、周長比 ＝ 相似比；<b>面積比 ＝ 相似比的平方</b>。" + ade({("A", "D"): "4", ("D", "B"): "2", ("D", "E"): "6", ("B", "C"): "x"})],
        [example("上圖 %s // %s，求 x" % (ov("DE"), ov("BC")), ["%s：%s ＝ 4：6 ＝ 6：x。" % (ov("AD"), ov("AB"))], "x ＝ 9"),
         example("相似比 2：3，小三角形面積 8，大三角形面積？", ["面積比 4：9。", "8 ÷ 4 × 9。"], "18")],
        [("用 %s：%s ＝ %s：%s" % (ov("AD"), ov("DB"), ov("DE"), ov("BC")), "要用整條 %s，不是 %s" % (ov("AB"), ov("DB"))),
         ("相似比 2：3，面積比也是 2：3", "面積比是 4：9"),
         ("兩邊成比例、任一角相等就相似", "要是夾角（SAS）")])
    faq = [{"q": "為什麼面積比是相似比的平方？",
            "a": "面積 ＝ 底 × 高 ÷ 2，底和高都按相似比放大，兩個相乘，所以面積放大相似比的平方倍。"},
           {"q": "AA 為什麼只要兩個角？",
            "a": "三角形內角和是 180°，兩個角相等，第三個角也一定相等，形狀就確定了。"},
           {"q": "九年級的三角形相似要學什麼？",
            "a": "108課綱 S-9-2：AA、SAS、SSS 相似判定，對應高之比、面積比與相似比的關係，相似符號 ～ 和應用問題。"}]
    make_unit(R, "grade-9", "similar-triangles", "S-9-2",
              "三角形的相似性質：三角形的相似判定（AA、SAS、SSS）；對應邊長之比＝對應高之比；對應面積之比＝對應邊長平方之比；利用三角形相似的概念解應用問題；相似符號（～）。",
              "三角形的相似性質",
              "九年級數學 相似三角形 練習題｜AA・SAS・SSS・面積比 學習單（附解答）",
              "相似三角形",
              "國中九年級數學「三角形的相似性質」免費學習單：AA、SAS、SSS 相似判定，平行線截出相似三角形求邊長，對應邊，面積比等於相似比平方，影子與鏡子測高應用題。100題線上練習馬上對答案，附可列印解答。",
              "AA、SAS、SSS；面積比 ＝ 相似比的平方",
              "DE // BC 時 △ADE ～ △ABC，要用整條 AB 來比。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
