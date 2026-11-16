# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：三角形的外心（108課綱 S-9-8）
  python3 tools/gen_tw_math_g9_circumcenter.py
外心＝三邊の中垂線の交點、三頂點まで等距離（外接圓の半徑）、銳角・直角・鈍角三角形で外心の位置、直角三角形は斜邊の中點、∠BOC ＝ 2∠A、正三角形の外接圓半徑。
誤答：外心と內心の取り違え（角平分線）、直角三角形の外接圓半徑を斜邊にする、∠BOC を ∠A と同じにする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr
from tw_g7 import tidy_sets
from tw_g9 import ov, pi

R = random.Random(81109)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26), (20, 21, 29), (12, 35, 37), (9, 40, 41), (16, 30, 34), (18, 24, 30)]


def s1(seen):
    FACTS = [("三角形的外心是哪三條線的交點？", "三邊的中垂線", ["三個內角的角平分線", "三條中線", "三條高"], "外心是三邊中垂線的交點。"),
             ("三角形的外心到什麼的距離相等？", "三個頂點", ["三邊", "三邊的中點", "三條中線"], "中垂線上的點到線段兩端等距，所以外心到三個頂點等距。"),
             ("銳角三角形的外心在哪裡？", "三角形內部", ["三角形外部", "斜邊中點", "某個頂點上"], "銳角三角形的外心在內部。"),
             ("直角三角形的外心在哪裡？", "斜邊的中點", ["直角的頂點", "三角形內部", "三角形外部"], "直角三角形的外心是斜邊中點，外接圓半徑是斜邊的一半。"),
             ("鈍角三角形的外心在哪裡？", "三角形外部", ["三角形內部", "最長邊的中點", "鈍角的頂點"], "鈍角三角形的外心在外部（最長邊的外側）。"),
             ("以三角形外心為圓心、到頂點的距離為半徑畫的圓叫什麼？", "外接圓", ["內切圓", "同心圓", "單位圓"], "這個圓通過三個頂點，叫外接圓。"),
             ("正三角形的外心和重心、內心的關係是？", "三心重合（同一點）", ["外心在外部", "三點在同一直線但不重合", "沒有關係"], "正三角形的中垂線、角平分線、中線是同一組線，三心重合。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def kind():
        a, b = R.randint(20, 80), R.randint(20, 80)
        c = 180 - a - b
        if c <= 0 or 90 in (a, b, c):
            return None
        mx = max(a, b, c)
        ans = "三角形內部" if mx < 90 else "三角形外部"
        q = "△ABC 中，∠A ＝ %d°，∠B ＝ %d°，它的外心在哪裡？" % (a, b)
        return mcq(q, ans, ["三角形外部" if mx < 90 else "三角形內部", "斜邊的中點", "頂點 C 上"], "∠C ＝ %d°，最大角 %d° 是%s角，外心在%s。" % (c, mx, "銳" if mx < 90 else "鈍", ans))
    return out + pick_unique(R, kind, 13, seen)


def s2(seen):
    def mk():
        a, b, c = R.choice(TRIP)
        t = R.choice(["R", "dist"])
        if t == "R":
            q = "直角三角形的兩股是 %d 和 %d，外接圓半徑是多少？" % (a, b)
            r = c / 2
            return mcq(q, "%g" % r, ["%g" % x for x in (c, (a + b) / 2, (a + b - c) / 2)], "斜邊 √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d，外心是斜邊中點，半徑 ＝ %g。" % (a, b, c, r))
        q = "直角三角形 ABC 中 ∠C ＝ 90°，斜邊 %s ＝ %d，外心 O 到 C 的距離是多少？" % (ov("AB"), c)
        return mcq(q, "%g" % (c / 2), ["%g" % x for x in (c, a, c / 3)], "外心 O 是斜邊中點，到三個頂點等距：%s ＝ %d ÷ 2 ＝ %g。" % (ov("OC"), c, c / 2))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = R.randint(20, 85)
        t = R.choice(["BOC", "A"])
        if t == "BOC":
            q = "銳角三角形 ABC 的外心是 O，∠A ＝ %d°，∠BOC 是多少度？" % a
            return mcq(q, "%d°" % (2 * a), ["%d°" % x for x in (a, 180 - a, 90 + a // 2 if 90 + a // 2 != 2 * a else a + 30)], "∠BOC 是外接圓的圓心角，∠A 是同弧的圓周角：∠BOC ＝ 2 × %d° ＝ %d°。" % (a, 2 * a))
        b = 2 * a
        q = "銳角三角形 ABC 的外心是 O，∠BOC ＝ %d°，∠A 是多少度？" % b
        return mcq(q, "%d°" % a, ["%d°" % x for x in (b, 180 - b if 180 - b > 0 and 180 - b != a else a + 15, (b - 90) * 2 if 0 < (b - 90) * 2 < 180 and (b - 90) * 2 != a else a + 10)], "∠A ＝ ∠BOC ÷ 2 ＝ %d°。" % a)

    def iso():
        c = R.randint(30, 160)
        if c % 2:
            return None
        q = "△ABC 的外心是 O，∠BOC ＝ %d°，∠OBC 是多少度？" % c
        v = (180 - c) // 2
        return mcq(q, "%d°" % v, ["%d°" % x for x in (c // 2, 180 - c, v + 10)], "%s ＝ %s，△OBC 是等腰三角形：（180° － %d°）÷ 2 ＝ %d°。" % (ov("OB"), ov("OC"), c, v))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, iso, 8, seen)


def s4(seen):
    def eq():
        k = R.randint(1, 12)
        a = 3 * k
        q = "邊長 %d 的正三角形，外接圓半徑是多少？" % a
        r = "%d√3" % k if k > 1 else "√3"
        return mcq(q, r, [fr("%d√3" % a, 2), "%d√3" % (2 * k), fr("%s√3" % ("" if k == 1 else k), 2), "%d√3" % a], "正三角形的外心也是重心，半徑 ＝ 高的 <span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span>：高 <span class='fr'><span class='fn'>%d√3</span><span class='fd'>2</span></span>，半徑 ＝ %s。" % (a, r))

    def area():
        a, b, c = R.choice(TRIP[:10])
        q = "直角三角形的兩股是 %d 和 %d，外接圓的面積是多少？" % (a, b)
        from fractions import Fraction as F
        A = F(c * c, 4)
        return mcq(q, pi(A), [pi(c * c), pi(F(c, 2)), pi(F((a + b) ** 2, 4))], "外接圓半徑 ＝ 斜邊 ÷ 2 ＝ %g，面積 ＝ π ×（%g）<sup>2</sup> ＝ %s。" % (c / 2, c / 2, pi(A)))
    return pick_unique(R, eq, 10, seen) + pick_unique(R, area, 10, seen)


def s5(seen):
    def app():
        q, a, w, e = R.choice([
            ("三個村莊位在三角形的三個頂點，要蓋一座到三個村莊距離相等的水塔，水塔應蓋在三角形的哪裡？", "外心", ["內心", "重心", "最長邊的中點"], "到三個頂點等距的點是外心。"),
            ("在三角形空地上找一點裝灑水器，要剛好能灑到三個角落（到三個頂點一樣遠），應裝在哪裡？", "外心", ["內心", "重心", "最長邊的中點"], "到三個頂點等距是外心。"),
            ("要找一個圓剛好通過三角形的三個頂點，圓心要找三角形的哪一個心？", "外心", ["內心", "重心", "任一頂點"], "通過三頂點的圓是外接圓，圓心是外心。"),
        ])
        return mcq(q, a, w, e)

    def coord():
        a, b, c = R.choice(TRIP[:8])
        x0, y0 = R.randint(-5, 5), R.randint(-5, 5)
        if a % 2 or b % 2:
            return None
        q = "坐標平面上直角三角形的頂點是（%d，%d）、（%d，%d）、（%d，%d），外心的坐標是？" % (x0, y0, x0 + a, y0, x0, y0 + b)
        cx, cy = x0 + a // 2, y0 + b // 2
        return mcq(q, "（%d，%d）" % (cx, cy), ["（%d，%d）" % p for p in ((x0, y0), (x0 + a // 3, y0 + b // 3), (cx, y0))], "直角頂點是（%d，%d），外心是斜邊中點：（%d，%d）。" % (x0, y0, cx, cy))
    out = []
    seen_local = set()
    for _ in range(40):
        it = app()
        if it["q"] not in seen_local:
            seen_local.add(it["q"])
            out.append(it)
    for b in out:
        seen.add(b["q"])
    return out + pick_unique(R, coord, 20 - len(out), seen)


def main():
    seen = set()
    sets = [("認識外心", s1(seen)), ("直角三角形的外心", s2(seen)), ("外心與角度", s3(seen)),
            ("外接圓", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["三角形<b>三邊中垂線的交點叫外心</b>。外心到三個頂點的距離相等，是外接圓的圓心。",
         "外心的位置：銳角三角形在內部，<b>直角三角形在斜邊中點</b>（外接圓半徑 ＝ 斜邊 ÷ 2），鈍角三角形在外部。",
         "銳角三角形中，外心 O 和頂點形成 <b>∠BOC ＝ 2∠A</b>（圓心角是圓周角的 2 倍）。"],
        [example("直角三角形兩股 6、8，外接圓半徑？", ["斜邊 10。", "10 ÷ 2。"], "5"),
         example("外心 O，∠A ＝ 50°，∠BOC？", ["2 × 50°。"], "100°")],
        [("外心是角平分線的交點", "那是內心；外心是中垂線的交點"),
         ("直角三角形外接圓半徑 ＝ 斜邊", "是斜邊的一半"),
         ("外心一定在三角形內部", "鈍角三角形的外心在外部")])
    faq = [{"q": "為什麼外心到三個頂點等距？",
            "a": "中垂線上的每一點到線段兩端的距離相等。外心同時在 AB、BC 的中垂線上，所以 OA ＝ OB ＝ OC。"},
           {"q": "怎麼找直角三角形的外心？",
            "a": "直接找斜邊的中點。因為直徑所對的圓周角是 90°，斜邊就是外接圓的直徑。"},
           {"q": "九年級的外心要學什麼？",
            "a": "108課綱 S-9-8：外心的意義與外接圓，外心到三頂點等距，直角三角形的外心是斜邊中點。"}]
    make_unit(R, "grade-9", "circumcenter", "S-9-8",
              "三角形的外心：外心的意義與外接圓；三角形的外心到三角形的三個頂點等距；直角三角形的外心即斜邊的中點。",
              "三角形的外心與外接圓",
              "九年級數學 三角形外心 練習題｜外接圓・中垂線・直角三角形斜邊中點 學習單（附解答）",
              "外心",
              "國中九年級數學「三角形的外心與外接圓」免費學習單：外心是中垂線的交點、到三頂點等距、直角三角形外心在斜邊中點、∠BOC＝2∠A、外接圓半徑與面積、水塔選址應用題。100題線上練習馬上對答案，附可列印解答。",
              "外心到三個頂點等距",
              "直角三角形的外心是斜邊中點，半徑 ＝ 斜邊 ÷ 2。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
