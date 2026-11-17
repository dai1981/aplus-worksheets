# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：空間中的線與平面（108課綱 S-9-12）
  python3 tools/gen_tw_math_g9_lines_and_planes_in_space.py
長方體 ABCD-EFGH の稜どうし（平行・相交・歪斜）、本數を數える、稜と面（在面上・平行・垂直）、面と面（平行・垂直）、正四面體、距離。
誤答：交わらなければ平行とする（歪斜を忘れる）、面上の線を平行とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fig, svg_wrap, text, line, INK, BLUE
from tw_g7 import tidy_sets
from tw_g9 import ov

R = random.Random(81117)
V = {"A": (0, 0, 1), "B": (1, 0, 1), "C": (1, 1, 1), "D": (0, 1, 1), "E": (0, 0, 0), "F": (1, 0, 0), "G": (1, 1, 0), "H": (0, 1, 0)}
EDGES = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]
FACES = ["ABCD", "EFGH", "ABFE", "DCGH", "BCGF", "ADHE"]


def vec(e):
    a, b = V[e[0]], V[e[1]]
    return tuple(b[i] - a[i] for i in range(3))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def rel(e1, e2):
    if set(e1) & set(e2):
        return "相交"
    if cross(vec(e1), vec(e2)) == (0, 0, 0):
        return "平行"
    return "歪斜"


def normal(f):
    a, b, c = V[f[0]], V[f[1]], V[f[2]]
    return cross(tuple(b[i] - a[i] for i in range(3)), tuple(c[i] - a[i] for i in range(3)))


def lp(e, f):
    if set(e) <= set(f):
        return "在平面上"
    n = normal(f)
    d = vec(e)
    if cross(d, n) == (0, 0, 0):
        return "垂直"
    if dot(d, n) == 0:
        return "平行"
    return "相交"


def pp(f1, f2):
    n1, n2 = normal(f1), normal(f2)
    return "平行" if cross(n1, n2) == (0, 0, 0) else "垂直"


def cuboid():
    P = {}
    for k, (x, y, z) in V.items():
        P[k] = (40 + x * 150 + y * 60, 168 - z * 100 - y * 45)
    hidden = {"H"}
    s = []
    for e in EDGES:
        (x1, y1), (x2, y2) = P[e[0]], P[e[1]]
        dash = " stroke-dasharray='5,4'" if set(e) & hidden else ""
        s.append(line(x1, y1, x2, y2, INK, 2, dash))
    OFF = {"A": (-12, 5), "B": (-10, 18), "C": (10, -4), "D": (0, -7), "E": (-12, 10), "F": (8, 16), "G": (13, 6), "H": (10, -6)}
    for k, (x, y) in P.items():
        dx, dy = OFF[k]
        s.append(text(x + dx, y + dy, k, 13))
    return fig(svg_wrap(270, 195, "".join(s), "長方體 ABCD-EFGH"))


FIG = None


def s1(seen):
    def mk():
        e1, e2 = R.sample(EDGES, 2)
        r = rel(e1, e2)
        q = "長方體 ABCD-EFGH 中，%s 和 %s 是什麼關係？" % (ov(e1), ov(e2)) + FIG
        why = {"相交": "兩條稜有共同的頂點 %s，所以相交（而且互相垂直）。" % "".join(set(e1) & set(e2)), "平行": "兩條稜在同一個平面上而且方向相同，不相交，所以平行。", "歪斜": "兩條稜不相交，也不在同一個平面上，所以是歪斜線。"}[r]
        return mcq(q, r, ["相交", "平行", "歪斜", "重合"], why)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        e = R.choice(EDGES)
        k = R.choice(["平行", "歪斜", "相交"])
        lst = [x for x in EDGES if x != e and rel(e, x) == k]
        q = "長方體 ABCD-EFGH 中，和 %s %s的稜有幾條？" % (ov(e), {"平行": "平行", "歪斜": "歪斜", "相交": "相交"}[k]) + FIG
        n = len(lst)
        return mcq(q, "%d 條" % n, ["%d 條" % x for x in {3, 4, 8, 2, 6} if x != n][:3], "%s：%s，共 %d 條。" % (k, "、".join(ov(x) for x in lst), n))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        e = R.choice(EDGES)
        f = R.choice(FACES)
        r = lp(e, f)
        q = "長方體 ABCD-EFGH 中，%s 和平面 %s 是什麼關係？" % (ov(e), f) + FIG
        why = {"在平面上": "%s 的兩個端點都在平面 %s 上，所以整條線在平面上。" % (ov(e), f), "垂直": "%s 和平面 %s 上過交點的兩條稜都垂直，所以垂直於這個平面。" % (ov(e), f), "平行": "%s 和平面 %s 沒有交點（它平行於平面上的一條稜），所以平行。" % (ov(e), f)}[r]
        return mcq(q, r, ["在平面上", "垂直", "平行", "歪斜"], why)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        f1, f2 = R.sample(FACES, 2)
        r = pp(f1, f2)
        q = "長方體 ABCD-EFGH 中，平面 %s 和平面 %s 是什麼關係？" % (f1, f2) + FIG
        return mcq(q, r, ["平行", "垂直", "歪斜", "重合"], "長方體相對的兩個面平行，相鄰的兩個面互相垂直：%s。" % ("相對的面，平行" if r == "平行" else "相鄰的面（交於一條稜），垂直"))

    def cnt():
        f = R.choice(FACES)
        k = R.choice(["垂直", "平行"])
        n = sum(1 for g in FACES if g != f and pp(f, g) == k)
        q = "長方體 ABCD-EFGH 中，和平面 %s %s的面有幾個？" % (f, k) + FIG
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in {1, 2, 4, 5} if x != n][:3], "長方體每個面有 1 個平行的對面和 4 個垂直的鄰面，所以是 %d 個。" % n)
    return pick_unique(R, mk, 12, seen) + pick_unique(R, cnt, 8, seen)


def s5(seen):
    FACTS = [("正四面體有幾條稜？", "6 條", ["4 條", "8 條", "12 條"], "正四面體有 4 個頂點，每兩個頂點連一條稜：6 條。"),
             ("正四面體有幾個面？每個面是什麼形狀？", "4 個，正三角形", ["4 個，正方形", "6 個，正三角形", "3 個，正三角形"], "正四面體由 4 個全等的正三角形圍成。"),
             ("正四面體 ABCD 中，" + ov("AB") + " 和 " + ov("CD") + " 是什麼關係？", "歪斜", ["平行", "相交", "垂直相交"], "AB 和 CD 沒有共同頂點，也不在同一個面上，是歪斜線。"),
             ("正四面體 ABCD 中，" + ov("AB") + " 和 " + ov("BC") + " 的夾角是多少度？", "60°", ["90°", "45°", "120°"], "它們是正三角形 ABC 的兩邊，夾角 60°。"),
             ("正四面體中，有幾對互相歪斜的稜？", "3 對", ["2 對", "4 對", "6 對"], "相對的稜（沒有共同頂點）互相歪斜：AB 和 CD、AC 和 BD、AD 和 BC，共 3 對。"),
             ("正四面體中有平行的稜嗎？", "沒有", ["有 3 對", "有 6 對", "有 1 對"], "任兩條稜不是相交就是歪斜，沒有平行的稜。"),
             ("長方體有幾對互相平行的面？", "3 對", ["2 對", "4 對", "6 對"], "上下、前後、左右各一對，共 3 對。"),
             ("長方體中，和一條稜歪斜的稜有幾條？", "4 條", ["2 條", "3 條", "8 條"], "12 條稜中，3 條平行、4 條相交、4 條歪斜（再加它自己 1 條）。"),
             ("兩條直線不相交，它們一定平行嗎？", "不一定，可能歪斜", ["一定平行", "一定垂直", "一定在同一平面"], "在空間中，不相交的兩條線可能平行，也可能是歪斜線。"),
             ("一條直線和平面上兩條相交直線都垂直，它和這個平面的關係是？", "垂直", ["平行", "在平面上", "歪斜"], "這是判斷直線垂直平面的方法。"),
             ("怎麼量一個點到一個平面的距離？", "量這點到平面的垂直線段長", ["量到平面上任一點的距離", "量到平面最遠點的距離", "量到平面邊緣的距離"], "點到平面的距離是垂直線段的長度，它是最短的。"),
             ("兩個平行平面之間的距離，處處都相等嗎？", "相等", ["不一定相等", "越遠越大", "只有中間相等"], "平行平面之間的垂直距離處處相等。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def dist():
        a, b, c = R.randint(2, 15), R.randint(2, 15), R.randint(2, 15)
        if len({a, b, c}) < 3:
            return None
        q = "長方體 ABCD-EFGH 中，%s ＝ %d，%s ＝ %d，%s ＝ %d。%s 到平面 EFGH 的距離是多少？" % (ov("AB"), a, ov("BC"), b, ov("AE"), c, ov("AB")) + FIG
        return mcq(q, str(c), [str(a), str(b), str(a + c)], "%s 垂直平面 EFGH，%s 到平面 EFGH 的距離就是 %s ＝ %d。" % (ov("AE"), ov("AB"), ov("AE"), c))
    return out + pick_unique(R, dist, 8, seen)


def main():
    global FIG
    FIG = cuboid()
    seen = set()
    sets = [("稜和稜的關係", s1(seen)), ("數一數", s2(seen)), ("線和平面", s3(seen)),
            ("面和面", s4(seen)), ("正四面體與距離", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["空間中兩條直線有三種關係：<b>相交</b>、<b>平行</b>（在同一平面、不相交）、<b>歪斜</b>（不相交，也不在同一平面）。",
         "直線和平面：<b>在平面上</b>、<b>平行</b>（沒有交點）、<b>相交</b>；如果和平面上兩條相交直線都垂直，就是<b>垂直</b>。",
         "兩個平面：<b>平行</b>或相交；長方體相對的面平行、相鄰的面垂直。" + FIG],
        [example("AB 和 GH 的關係", ["AB // DC // HG，所以平行。"], "平行"),
         example("AB 和 CG 的關係", ["沒有共同頂點，也不平行。"], "歪斜")],
        [("不相交就是平行", "可能是歪斜線"),
         ("AB 和平面 ABCD 平行", "AB 在平面 ABCD 上"),
         ("正四面體有平行的稜", "沒有，相對的稜是歪斜")])
    faq = [{"q": "怎麼判斷兩條稜是歪斜？",
            "a": "先看有沒有共同的頂點（有就是相交），再看是不是平行；兩個都不是，就是歪斜線。"},
           {"q": "長方體中和一條稜有關的稜各有幾條？",
            "a": "其他 11 條稜中，平行 3 條、相交 4 條、歪斜 4 條。"},
           {"q": "九年級的空間概念要學什麼？",
            "a": "108課綱 S-9-12：用長方體和正四面體認識線與線的平行、垂直與歪斜，線與平面的垂直和平行，面與面的關係。"}]
    make_unit(R, "grade-9", "lines-and-planes-in-space", "S-9-12",
              "空間中的線與平面：長方體與正四面體的示意圖，利用長方體與正四面體作為特例，介紹線與線的平行、垂直與歪斜關係，線與平面的垂直與平行關係。",
              "空間中的線與平面",
              "九年級數學 空間中的線與平面 練習題｜平行・垂直・歪斜線 學習單（附解答）",
              "空間中的線與平面",
              "國中九年級數學「空間中的線與平面」免費學習單：長方體中稜和稜的平行、相交、歪斜，數一數，線和平面、面和面的平行與垂直，正四面體和距離。100題線上練習馬上對答案，附可列印解答。",
              "兩條線：相交、平行或歪斜",
              "不相交也不在同一平面上的兩條線叫歪斜線。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
