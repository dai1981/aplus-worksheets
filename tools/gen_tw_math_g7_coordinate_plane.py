# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：平面直角坐標系（108課綱 G-7-1）
  python3 tools/gen_tw_math_g7_coordinate_plane.py
點の坐標を讀む（x 坐標が先）、象限（第一〜第四、軸上はどの象限にも屬さない）、軸に平行な二點の距離、對稱點（x 軸・y 軸・原點）、平移・方位距離の應用。
誤答：(x, y) を逆に讀む、軸上の點を象限に入れる、對稱で兩方の符號を變える、距離で絕對值を取らない。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, tidy_sets, opv
from tw_g7_grid import plane

R = random.Random(71017)
NM = Names(R)


def P(x, y):
    return "（%s, %s）" % (sn(x), sn(y))


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def quad(x, y):
    if x == 0 or y == 0:
        return "不在任何象限（在坐標軸上）"
    return {(1, 1): "第一象限", (-1, 1): "第二象限", (-1, -1): "第三象限", (1, -1): "第四象限"}[(1 if x > 0 else -1, 1 if y > 0 else -1)]


def s1(seen):
    def mk():
        x, y = nz(-6, 6), R.randint(-6, 6)
        g = plane(6, [(x, y, "A")])
        return mcq("A 點的坐標是多少？" + g, P(x, y), [P(y, x) if x != y else P(-x, y), P(-x, y), P(x, -y) if y else P(x, 1)], "先看橫軸 x ＝ %s，再看縱軸 y ＝ %s：A%s。" % (sn(x), sn(y), P(x, y)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    Q = ["第一象限", "第二象限", "第三象限", "第四象限", "不在任何象限（在坐標軸上）"]

    def mk():
        x, y = R.randint(-20, 20), R.randint(-20, 20)
        if (x == 0 or y == 0) and R.random() < .6:
            return None
        ans = quad(x, y)
        return mcq("點%s在哪裡？" % P(x, y), ans, [q for q in Q if q != ans][:3] if ans != Q[4] else Q[:3], "x 是%s、y 是%s：%s。" % ("正" if x > 0 else ("負" if x < 0 else "0"), "正" if y > 0 else ("負" if y < 0 else "0"), ans))

    def rule():
        F_ = [("第二象限的點，坐標的符號是？", "（－, ＋）", ["（＋, －）", "（－, －）", "（＋, ＋）"], "第二象限在左上：x 負、y 正。"),
              ("第四象限的點，坐標的符號是？", "（＋, －）", ["（－, ＋）", "（－, －）", "（＋, ＋）"], "第四象限在右下：x 正、y 負。"),
              ("x 軸上的點，哪一個坐標一定是 0？", "y 坐標", ["x 坐標", "兩個都是", "都不是"], "x 軸上的點高度是 0，所以 y ＝ 0。"),
              ("y 軸上的點，哪一個坐標一定是 0？", "x 坐標", ["y 坐標", "兩個都是", "都不是"], "y 軸上的點左右位置是 0，所以 x ＝ 0。"),
              ("原點的坐標是？", "（0, 0）", ["（1, 1）", "（0, 1）", "沒有坐標"], "原點是兩軸的交點。"),
              ("點（a, b）在第三象限，那麼點（－a, b）在第幾象限？", "第四象限", ["第一象限", "第二象限", "第三象限"], "a ＜ 0、b ＜ 0，所以 －a ＞ 0、b ＜ 0，在第四象限。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, rule, 6, seen)


def s3(seen):
    def mk():
        if R.random() < .5:
            x1, x2, y = R.sample(range(-9, 10), 2) + [R.randint(-9, 9)]
            d = abs(x1 - x2)
            q = "A%s和 B%s的距離是多少？" % (P(x1, y), P(x2, y))
            e = "y 坐標一樣，兩點在同一條水平線上，距離 ＝ ｜%s%s｜ ＝ %d。" % (sn(x1), opv("－", x2), d)
            w = [abs(abs(x1) - abs(x2)), abs(x1 + x2), d + 1]
        else:
            y1, y2, x = R.sample(range(-9, 10), 2) + [R.randint(-9, 9)]
            d = abs(y1 - y2)
            q = "A%s和 B%s的距離是多少？" % (P(x, y1), P(x, y2))
            e = "x 坐標一樣，兩點在同一條鉛垂線上，距離 ＝ ｜%s%s｜ ＝ %d。" % (sn(y1), opv("－", y2), d)
            w = [abs(abs(y1) - abs(y2)), abs(y1 + y2), d + 1]
        return mcq(q, str(d), [str(t) for t in w if t != d] + [str(d + 2)], e)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        x, y = nz(-9, 9), nz(-9, 9)
        k = R.choice(["x", "y", "o"])
        if k == "x":
            ans, name = P(x, -y), " x 軸"
        elif k == "y":
            ans, name = P(-x, y), " y 軸"
        else:
            ans, name = P(-x, -y), "原點"
        q = "點%s對稱於%s的點是？" % (P(x, y), name)
        w = [P(x, -y), P(-x, y), P(-x, -y), P(y, x)]
        return mcq(q, ans, [t for t in w if t != ans], {"x": "對稱於 x 軸：x 不變，y 變號。", "y": "對稱於 y 軸：y 不變，x 變號。", "o": "對稱於原點：x、y 都變號。"}[k])

    def move():
        x, y = nz(-6, 6), nz(-6, 6)
        r, u = nz(-5, 5), nz(-5, 5)
        q = "點%s先向%s移 %d 單位，再向%s移 %d 單位，新的坐標是？" % (P(x, y), "右" if r > 0 else "左", abs(r), "上" if u > 0 else "下", abs(u))
        ans = P(x + r, y + u)
        return mcq(q, ans, [P(x + u, y + r), P(x - r, y - u), P(x + r, y - u)], "左右改 x、上下改 y：x %s %d，y %s %d，得 %s。" % ("＋" if r > 0 else "－", abs(r), "＋" if u > 0 else "－", abs(u), ans))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, move, 10, seen)


def s5(seen):
    def area():
        x1, x2 = sorted(R.sample(range(-6, 7), 2))
        y1, y2 = sorted(R.sample(range(-6, 7), 2))
        w, h = x2 - x1, y2 - y1
        pts = [(x1, y1, "A"), (x2, y1, "B"), (x2, y2, "C"), (x1, y2, "D")]
        g = plane(6, pts, [((x1, y1), (x2, y1), "#3f7fbf"), ((x2, y1), (x2, y2), "#3f7fbf"), ((x2, y2), (x1, y2), "#3f7fbf"), ((x1, y2), (x1, y1), "#3f7fbf")])
        q = "長方形 ABCD 的頂點是 A%s、B%s、C%s、D%s。面積是多少？" % (P(x1, y1), P(x2, y1), P(x2, y2), P(x1, y2)) + g
        return mcq(q, str(w * h), [str(t) for t in (2 * (w + h), w + h, abs(x1 * y1) + abs(x2 * y2))  if t != w * h] + [str(w * h + w)], "長 ＝ ｜%s%s｜ ＝ %d，寬 ＝ ｜%s%s｜ ＝ %d，面積 %d × %d ＝ %d。" % (sn(x2), opv("－", x1), w, sn(y2), opv("－", y1), h, w, h, w * h))

    def tri():
        x1, x2 = sorted(R.sample(range(-6, 7), 2))
        y0 = R.randint(-6, 6)
        x3, y3 = R.randint(-6, 6), R.choice([v for v in range(-6, 7) if v != y0])
        b, h = x2 - x1, abs(y3 - y0)
        if (b * h) % 2:
            return None
        g = plane(6, [(x1, y0, "A"), (x2, y0, "B"), (x3, y3, "C")], [((x1, y0), (x2, y0), "#3f7fbf"), ((x2, y0), (x3, y3), "#3f7fbf"), ((x3, y3), (x1, y0), "#3f7fbf")])
        q = "三角形 ABC 的頂點是 A%s、B%s、C%s。面積是多少？" % (P(x1, y0), P(x2, y0), P(x3, y3)) + g
        return mcq(q, str(b * h // 2), [str(t) for t in (b * h, b + h, b * abs(y3) // 2 if (b * abs(y3)) % 2 == 0 else b * h // 2 + 1)  if t != b * h // 2] + [str(b * h // 2 + 2)], "AB 在水平線上，底 ＝ %d；高 ＝ C 到 AB 的距離 ＝ %d；面積 %d × %d ÷ 2 ＝ %d。" % (b, h, b, h, b * h // 2))
    return pick_unique(R, area, 10, seen) + pick_unique(R, tri, 10, seen)


def main():
    seen = set()
    sets = [("讀出點的坐標", s1(seen)), ("象限", s2(seen)), ("水平和鉛垂的距離", s3(seen)),
            ("對稱點與平移", s4(seen)), ("坐標與面積", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["坐標平面由<b>橫軸（x 軸）</b>和<b>縱軸（y 軸）</b>組成，交點是原點 O（0, 0）。",
         "點的坐標寫成（x, y）：<b>先橫後縱</b>，先看左右，再看上下。",
         "四個象限：第一（＋, ＋）、第二（－, ＋）、第三（－, －）、第四（＋, －）。坐標軸上的點不屬於任何象限。",
         "y 坐標相同的兩點，距離 ＝ ｜x<sub>1</sub> － x<sub>2</sub>｜；x 坐標相同，距離 ＝ ｜y<sub>1</sub> － y<sub>2</sub>｜。"],
        [example("（－3, 2）在第幾象限？", ["x 負、y 正。"], "第二象限"),
         example("A（－2, 3）和 B（5, 3）的距離？", ["y 一樣，｜－2 － 5｜ ＝ 7。"], "7")],
        [("（3, －2）讀成往上 3、往右 －2", "先橫後縱：往右 3、往下 2"),
         ("（0, 4）在第一象限", "在 y 軸上，不屬於任何象限"),
         ("對稱於 x 軸，x 和 y 都變號", "只有 y 變號")])
    faq = [{"q": "坐標（x, y）要怎麼記？",
            "a": "先橫後縱：第一個數是左右（x），第二個數是上下（y）。從原點出發，先左右走，再上下走。"},
           {"q": "坐標軸上的點在哪個象限？",
            "a": "不屬於任何象限。例如（3, 0）在 x 軸上、（0, －2）在 y 軸上。"},
           {"q": "七年級的坐標平面要學什麼？",
            "a": "108課綱 G-7-1：以平面直角坐標系、方位距離標定位置，認識縱軸、橫軸、象限等術語。"}]
    make_unit(R, "grade-7", "coordinate-plane", "G-7-1",
              "平面直角坐標系：以平面直角坐標系、方位距離標定位置；平面直角坐標系及其相關術語（縱軸、橫軸、象限）。",
              "平面直角坐標系",
              "七年級數學 坐標平面 練習題｜象限・兩點距離・對稱點 學習單（附解答）",
              "坐標平面",
              "國中七年級數學「平面直角坐標系」免費學習單：讀出點的坐標、四個象限、水平和鉛垂兩點的距離、對稱點與平移，以及用坐標求長方形和三角形面積。100題線上練習馬上對答案，附可列印解答。",
              "坐標（x, y）：先橫後縱",
              "坐標軸上的點不屬於任何象限。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
