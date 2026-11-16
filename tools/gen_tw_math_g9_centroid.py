# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：三角形的重心（108課綱 S-9-10）
  python3 tools/gen_tw_math_g9_centroid.py
重心＝三條中線の交點、重心は中線を 2：1 に分ける、三條中線で面積六等分、座標で重心（平均）、正三角形・直角三角形の重心、重心の物理的意味。
誤答：AG：GD を 1：2 にする、面積を三等分とする、重心を外心と取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets, sn, par


def plus(vs):
    return " ＋ ".join([sn(vs[0])] + [par(v) for v in vs[1:]])
from tw_g9 import ov

R = random.Random(81111)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26), (18, 24, 30)]


def s1(seen):
    FACTS = [("三角形的重心是哪三條線的交點？", "三條中線", ["三邊的中垂線", "三個內角的角平分線", "三條高"], "中線是頂點到對邊中點的線段，三條中線交於重心。"),
             ("三角形的重心一定在哪裡？", "三角形內部", ["三角形外部", "最長邊上", "看是什麼三角形"], "重心一定在三角形內部。"),
             ("用一根手指頂住三角形紙板，在哪一點可以平衡？", "重心", ["外心", "內心", "最長邊的中點"], "重心是三角形的平衡點。"),
             ("三角形的三條中線把三角形分成幾個面積相等的小三角形？", "6 個", ["3 個", "4 個", "2 個"], "三條中線把三角形分成 6 個面積相等的小三角形。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def mk():
        m = R.randint(2, 20) * 3
        t = R.choice(["AG", "GD", "AD"])
        if t == "AG":
            q = "G 是 △ABC 的重心，%s 是中線，%s ＝ %d，%s 是多少？" % (ov("AD"), ov("AD"), m, ov("AG"))
            return mcq(q, str(2 * m // 3), [str(m // 3), str(m // 2) if m % 2 == 0 else str(m // 3 + 1), str(m)], "重心把中線分成 2：1，%s ＝ %d × <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> ＝ %d。" % (ov("AG"), m, 2 * m // 3))
        if t == "GD":
            q = "G 是 △ABC 的重心，%s 是中線，%s ＝ %d，%s 是多少？" % (ov("AD"), ov("AG"), 2 * m // 3, ov("GD"))
            return mcq(q, str(m // 3), [str(2 * m // 3 * 2), str(m), str(m // 3 + 1)], "%s：%s ＝ 2：1，%s ＝ %d ÷ 2 ＝ %d。" % (ov("AG"), ov("GD"), ov("GD"), 2 * m // 3, m // 3))
        q = "G 是 △ABC 的重心，%s 是中線，%s ＝ %d，%s 是多少？" % (ov("AD"), ov("GD"), m // 3, ov("AD"))
        return mcq(q, str(m), [str(2 * m // 3), str(m // 3 * 2 + 1), str(m // 3 * 4)], "%s ＝ 2 × %s，%s ＝ 3 × %d ＝ %d。" % (ov("AG"), ov("GD"), ov("AD"), m // 3, m))
    return out + pick_unique(R, mk, 16, seen)


def s2(seen):
    def mk():
        A = R.randint(2, 30) * 6
        t = R.choice(["GBD", "ABD", "GBC", "AGB"])
        v = {"GBD": A // 6, "ABD": A // 2, "GBC": A // 3, "AGB": A // 3}[t]
        why = {"GBD": "三條中線把三角形分成 6 個面積相等的小三角形，△GBD 是其中 1 個：%d ÷ 6 ＝ %d。",
               "ABD": "中線 AD 把三角形分成面積相等的兩半：%d ÷ 2 ＝ %d。",
               "GBC": "△GBC 由 2 個小三角形組成：%d ÷ 6 × 2 ＝ %d。" ,
               "AGB": "△AGB 由 2 個小三角形組成：%d ÷ 6 × 2 ＝ %d。"}[t]
        q = "G 是 △ABC 的重心，D 是 %s 的中點，△ABC 的面積是 %d，△%s 的面積是多少？" % (ov("BC"), A, t)
        return mcq(q, str(v), [str(x) for x in {A // 6, A // 2, A // 3, A // 4} if x != v], why % (A, v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        pts = [(R.randint(-8, 10), R.randint(-8, 10)) for _ in range(3)]
        sx, sy = sum(p[0] for p in pts), sum(p[1] for p in pts)
        if sx % 3 or sy % 3:
            return None
        g = (sx // 3, sy // 3)
        q = "△ABC 的頂點 A（%s，%s）、B（%s，%s）、C（%s，%s），重心 G 的坐標是？" % tuple(sn(v) for p in pts for v in p)
        w = [(sx, sy), (sx // 2 if sx % 2 == 0 else g[0] + 1, sy // 2 if sy % 2 == 0 else g[1] + 1), (g[1], g[0]) if g[0] != g[1] else (g[0] + 1, g[1])]
        return mcq(q, "（%s，%s）" % (sn(g[0]), sn(g[1])), ["（%s，%s）" % (sn(a), sn(b)) for a, b in w], "重心坐標是三個頂點坐標的平均：x ＝（%s）÷ 3 ＝ %s，y ＝（%s）÷ 3 ＝ %s。" % (plus([p[0] for p in pts]), sn(g[0]), plus([p[1] for p in pts]), sn(g[1])))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def right():
        a, b, c = R.choice(TRIP)
        cg = R.random() < .3
        if cg and c % 3:
            return None
        m = c / 2
        if cg:
            q = "直角三角形 ABC 中 ∠C ＝ 90°，兩股 %d 和 %d，G 是重心，%s 是多少？" % (a, b, ov("CG"))
            v = c / 3
            return mcq(q, "%g" % v, ["%g" % x for x in (m, c / 6, c)], "斜邊 %d，斜邊上的中線 ＝ 斜邊的一半 ＝ %g，%s ＝ %g × <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> ＝ %g。" % (c, m, ov("CG"), m, v))
        q = "直角三角形 ABC 中 ∠C ＝ 90°，兩股 %d 和 %d，斜邊上的中線長多少？" % (a, b)
        return mcq(q, "%g" % m, ["%g" % x for x in (c, (a + b) / 2, a, b)], "斜邊 √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d；直角三角形斜邊中點是外心，斜邊上的中線 ＝ 斜邊的一半 ＝ %g。" % (a, b, c, m))

    def eq():
        k = R.randint(1, 10)
        a = 2 * k * 3 // 3 * 1
        side = 6 * k
        q = "邊長 %d 的正三角形，重心到頂點的距離是多少？" % side
        return mcq(q, "%d√3" % (2 * k), ["%d√3" % (3 * k), "%d√3" % k if k > 1 else "√3", "%d" % (4 * k)], "高 ＝ %d√3，重心到頂點 ＝ 高的 <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> ＝ %d√3。" % (3 * k, 2 * k))
    return pick_unique(R, right, 10, seen) + pick_unique(R, eq, 10, seen)


def s5(seen):
    CMP = [("外心", "三邊的中垂線", "到三個頂點等距"), ("內心", "三個內角的角平分線", "到三邊等距"), ("重心", "三條中線", "把中線分成 2：1")]
    out = []
    for name, ln, prop in CMP:
        out.append(mcq("三角形的%s是哪三條線的交點？（比較三心）" % name, ln, [x[1] for x in CMP if x[0] != name] + ["三條高"], "%s是%s的交點，%s。" % (name, ln, prop)))
        out.append(mcq("哪一個心有「%s」的性質？" % prop, name, [x[0] for x in CMP if x[0] != name] + ["垂足"], "%s：%s的交點，%s。" % (name, ln, prop)))
    out.append(mcq("哪一種三角形的外心、內心、重心是同一點？", "正三角形", ["直角三角形", "等腰三角形", "鈍角三角形"], "正三角形的中垂線、角平分線、中線重合，三心是同一點。"))
    out.append(mcq("等腰三角形的外心、內心、重心有什麼關係？", "都在底邊的中垂線上", ["三點重合", "都在腰上", "沒有關係"], "等腰三角形底邊的中垂線也是頂角平分線和中線，三心都在它上面。"))
    for b in out:
        seen.add(b["q"])

    def med():
        m = R.randint(2, 15) * 3
        q = "G 是 △ABC 的重心，%s ＝ %d，%s ＝ %d，%s ＝ %d，三條中線長的和是多少？" % (ov("AG"), 2 * m // 3, ov("BG"), 2 * (m // 3 + 1), ov("CG"), 2 * (m // 3 + 2))
        tot = (2 * m // 3 + 2 * (m // 3 + 1) + 2 * (m // 3 + 2)) * 3 // 2
        sg = 2 * m // 3 + 2 * (m // 3 + 1) + 2 * (m // 3 + 2)
        return mcq(q, str(tot), [str(sg), str(sg * 3), str(sg + sg // 4)], "每條中線 ＝ 頂點到重心 × <span class='fr'><span class='fn'>3</span><span class='fd'>2</span></span>：%d × <span class='fr'><span class='fn'>3</span><span class='fd'>2</span></span> ＝ %d。" % (sg, tot))
    return out + pick_unique(R, med, 20 - len(out), seen)


def main():
    seen = set()
    sets = [("中線與重心", s1(seen)), ("面積六等分", s2(seen)), ("重心的坐標", s3(seen)),
            ("直角三角形與正三角形", s4(seen)), ("三心的比較", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["頂點和對邊中點的連線叫<b>中線</b>，<b>三條中線的交點叫重心</b>，是三角形的平衡點，一定在內部。",
         "<b>重心把中線分成 2：1</b>：重心到頂點的距離是它到對邊中點的 2 倍。",
         "<b>三條中線把三角形面積六等分</b>；坐標平面上，重心坐標是三頂點坐標的平均。"],
        [example("中線 AD ＝ 18，AG？", ["AG ＝ 18 × 2/3。"], "12"),
         example("△ABC 面積 48，△GBD？", ["六等分。", "48 ÷ 6。"], "8")],
        [("AG：GD ＝ 1：2", "重心離頂點較遠：AG：GD ＝ 2：1"),
         ("三條中線把面積三等分", "是六等分"),
         ("重心到三頂點等距", "到三頂點等距的是外心")])
    faq = [{"q": "重心的物理意義是什麼？",
            "a": "把三角形紙板放在重心上，它會保持平衡，因為重心兩側的面積（重量）分配均勻。"},
           {"q": "為什麼重心把中線分成 2：1？",
            "a": "連接兩邊中點的線段平行第三邊且是它的一半，由相似三角形可得 AG：GD ＝ 2：1。"},
           {"q": "九年級的重心要學什麼？",
            "a": "108課綱 S-9-10：重心的意義與中線，三條中線將三角形面積六等分，重心到頂點的距離等於它到對邊中點的兩倍，以及重心的物理意義。"}]
    make_unit(R, "grade-9", "centroid", "S-9-10",
              "三角形的重心：重心的意義與中線；三角形的三條中線將三角形面積六等分；重心到頂點的距離等於它到對邊中點的兩倍；重心的物理意義。",
              "三角形的重心與中線",
              "九年級數學 三角形重心 練習題｜中線 2：1・面積六等分・三心比較 學習單（附解答）",
              "重心",
              "國中九年級數學「三角形的重心與中線」免費學習單：重心把中線分成 2：1、三條中線面積六等分、重心坐標、直角三角形與正三角形的重心、外心內心重心比較。100題線上練習馬上對答案，附可列印解答。",
              "重心把中線分成 2：1",
              "三條中線把三角形面積六等分。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
