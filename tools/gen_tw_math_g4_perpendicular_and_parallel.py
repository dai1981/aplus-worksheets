# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：垂直與平行（108課綱 S-4-5）
  python3 tools/gen_tw_math_g4_perpendicular_and_parallel.py
垂直・平行の線を見分ける（斜めに置いた図も）、四邊形の垂直・平行の辺、性質（同じ線に垂直な2線は平行、平行線の距離は等しい）、應用。
誤答：斜めの垂直を垂直でないと思う、交わっていない短い線を平行と思い込む、少し開いた線を平行とする。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK, RED, BLUE

R = random.Random(41016)
NM = Names(R)
LET = "甲乙丙丁"


def pair_svg(kinds):
    """kinds：'perp'、'para'、'none'（斜めに交わる）、'near'（ほとんど平行だが開いていく）を 4 つ"""
    s = []
    for i, k in enumerate(kinds):
        cx, cy = 60 + i * 120, 70
        rot = math.radians(R.choice([0, 15, 30, -20, 45, 70]))
        def seg(ang, ox=0, oy=0, L=46):
            dx, dy = L * math.cos(ang), L * math.sin(ang)
            return line(cx + ox - dx, cy + oy - dy, cx + ox + dx, cy + oy + dy, INK, 2.5)
        if k == "perp":
            s += [seg(rot), seg(rot + math.pi / 2)]
        elif k == "none":
            s += [seg(rot), seg(rot + math.radians(R.choice([55, 65, 115, 125])))]
        elif k == "para":
            nx, ny = -math.sin(rot) * 16, math.cos(rot) * 16
            s += [seg(rot, nx, ny), seg(rot, -nx, -ny)]
        else:
            nx, ny = -math.sin(rot) * 14, math.cos(rot) * 14
            s += [seg(rot + math.radians(6), nx, ny), seg(rot - math.radians(6), -nx, -ny)]
        s.append(text(cx, 140, LET[i], 16))
    return fig(svg_wrap(480, 150, "".join(s), "甲乙丙丁四組直線"))


def s1(seen):
    def mk():
        others = R.sample(["none", "none", "para", "near"], 3)
        kinds = others + ["perp"]
        R.shuffle(kinds)
        k = kinds.index("perp")
        q = "哪一組的兩條直線互相<b>垂直</b>？" + pair_svg(kinds)
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "兩條直線相交成直角（90 度），就是互相垂直。斜放也一樣，可以用三角板的直角檢查：%s。" % LET[k])
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        others = R.sample(["none", "perp", "near", "perp"], 3)
        kinds = others + ["para"]
        R.shuffle(kinds)
        k = kinds.index("para")
        q = "哪一組的兩條直線互相<b>平行</b>？" + pair_svg(kinds)
        near = [LET[i] for i, x in enumerate(kinds) if x == "near"]
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "兩條直線之間的距離處處相等、永遠不會相交，就是平行：%s。%s" % (LET[k], "%s看起來很像，但兩條線越來越開，延長後會相交。" % near[0] if near else ""))
    return pick_unique(R, mk, 20, seen)


SH = [("長方形", 2, 4), ("正方形", 2, 4), ("平行四邊形（沒有直角）", 2, 0), ("菱形（沒有直角）", 2, 0), ("梯形（沒有直角）", 1, 0), ("直角梯形（有 2 個直角）", 1, 2), ("直角三角形", 0, 1), ("正三角形", 0, 0), ("正六邊形", 3, 0), ("房子形狀的五邊形（下面是長方形）", 1, 2)]


def s3(seen):
    def mk():
        name, par, perp = R.choice(SH)
        if R.random() < .5:
            q = "%s有幾組互相平行的邊？" % name
            return mcq(q, "%d 組" % par, ["%d 組" % x for x in (0, 1, 2, 3, 4) if x != par][:3], "%s：%s。" % (name, {3: "三組對邊都平行", 2: "兩組對邊都平行", 1: "只有一組邊平行", 0: "沒有平行的邊"}[par]))
        q = "%s有幾個直角（相鄰兩邊互相垂直的地方）？" % name
        return mcq(q, "%d 個" % perp, ["%d 個" % x for x in (0, 1, 2, 4, 3) if x != perp][:3], "相鄰兩邊互相垂直就形成直角。%s有 %d 個。" % (name, perp))

    def which():
        F = [("哪一個圖形有兩組平行的邊，而且四個角都是直角？", "長方形", ["梯形", "菱形（沒有直角）", "三角形"]),
             ("哪一個圖形只有一組平行的邊？", "梯形", ["長方形", "平行四邊形", "正方形"]),
             ("哪一個圖形沒有平行的邊？", "三角形", ["長方形", "梯形", "平行四邊形"])]
        f = R.choice(F)
        return mcq(f[0], f[1], f[2], "看對邊有沒有平行：%s。" % f[1])
    out = pick_unique(R, mk, 12, seen)
    return out + pick_unique(R, which, 3, seen) + pick_unique(R, mk, 5, seen)


TRUE = ["兩條直線相交成直角，就是互相垂直。", "垂直於同一條直線的兩條直線互相平行。", "兩條平行線之間的距離處處相等。",
        "互相平行的兩條直線永遠不會相交。", "直角是 90 度。", "長方形相鄰的兩邊互相垂直。", "長方形相對的兩邊互相平行。"]
FALSE = ["斜放的兩條直線就不能互相垂直。", "兩條平行線之間的距離有遠有近。", "沒有畫到相交的兩條直線一定互相平行。",
         "垂直於同一條直線的兩條直線一定會相交。", "梯形有兩組平行的邊。", "直角是 180 度。", "長方形相鄰的兩邊互相平行。"]


def s4(seen):
    def mk():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s相交成直角是垂直；平行線距離處處相等、永不相交；垂直於同一條線的兩條線互相平行。" % (LET[k], ans))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def dist():
        d = R.randint(2, 12)
        q = "兩條平行線，在左邊量出它們的距離是 %d 公分，在右邊量會是幾公分？" % d
        return mcq(q, "%d 公分" % d, ["%d 公分" % x for x in (d + 1, d * 2, d - 1 if d > 2 else d + 2)] + ["不一定"], "平行線之間的距離處處相等，還是 %d 公分。" % d)

    def angles():
        q = R.choice([("直線甲和直線乙互相垂直，它們相交形成的 4 個角各是幾度？", "都是 90 度", ["都是 180 度", "兩個 90 度、兩個 180 度", "不一定"]),
                      ("直線甲垂直於直線丙，直線乙也垂直於直線丙，甲和乙是什麼關係？", "互相平行", ["互相垂直", "一定相交", "不一定"]),
                      ("直線甲和直線乙互相平行，直線丙垂直於甲，丙和乙是什麼關係？", "互相垂直", ["互相平行", "不會相交", "不一定"])])
        return mcq(q[0], q[1], q[2], "垂直相交的 4 個角都是 90 度；垂直於同一條線的兩條線平行；和平行線之一垂直，也和另一條垂直。")

    def ladder():
        n = R.randint(3, 9)
        gap = R.randint(20, 40)
        q = "梯子的每一根橫桿都互相平行，相鄰兩根相距 %d 公分。從第 1 根到第 %d 根相距幾公分？" % (gap, n)
        v = gap * (n - 1)
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (gap * n, gap * (n - 2), v + gap // 2)], "第 1 根到第 %d 根中間有 %d 段：%d × %d ＝ %d（公分）。" % (n, n - 1, gap, n - 1, v))

    def road():
        a = R.randint(20, 160)
        if a == 90:
            return None
        q = "兩條平行的馬路被第三條馬路斜斜穿過，在第一條路形成 %d 度的角，在第二條路同一個位置的角是幾度？" % a
        return mcq(q, "%d 度" % a, ["%d 度" % x for x in (180 - a, 90 - a if a < 90 else a - 90, a + 10)], "平行線被同一條直線穿過，同一個位置的角一樣大：%d 度。" % a)
    return pick_unique(R, dist, 6, seen) + pick_unique(R, angles, 3, seen) + pick_unique(R, ladder, 6, seen) + pick_unique(R, road, 5, seen)


def main():
    seen = set()
    sets = [("找出垂直的線", s1(seen)), ("找出平行的線", s2(seen)), ("圖形的垂直和平行", s3(seen)),
            ("垂直和平行的性質", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["兩條直線相交成<b>直角（90 度）</b>，叫做互相<b>垂直</b>。斜放的也可以垂直，用三角板的直角檢查。",
         "兩條直線<b>永遠不會相交</b>，叫做互相<b>平行</b>。平行線之間的距離<b>處處相等</b>。",
         "垂直於同一條直線的兩條直線，互相平行。",
         "長方形、正方形有兩組平行的邊，相鄰兩邊互相垂直；梯形只有一組平行的邊。"],
        [example("直線甲垂直於丙，直線乙也垂直於丙，甲和乙的關係？", ["甲、乙都和丙成 90 度。", "所以甲和乙方向一樣，永不相交。"], "互相平行"),
         example("平行四邊形有幾組平行的邊？", ["兩組對邊都平行。"], "2 組")],
        [("斜放的兩條線就不是垂直", "只要相交成 90 度就是垂直"),
         ("圖上沒有畫到相交，就一定平行", "要延長看看：越來越開或越來越近，就會相交"),
         ("梯形有兩組平行的邊", "梯形只有一組平行的邊")])
    faq = [{"q": "垂直和平行有什麼不同？",
            "a": "垂直是兩條線相交成 90 度；平行是兩條線永遠不相交，而且距離處處相等。"},
           {"q": "四年級的垂直與平行要學什麼？",
            "a": "108課綱 S-4-5：認識直角是 90 度和直角記號、垂直於一線的兩線互相平行、平行線間距離處處相等，並會用三角板畫垂直線和平行線。"},
           {"q": "怎麼用三角板畫平行線？",
            "a": "一個三角板的一邊貼著原來的直線，另一個三角板或直尺靠在旁邊固定，把第一個三角板沿著它滑動，再畫線，就是平行線。"}]
    make_unit(R, "grade-4", "perpendicular-and-parallel", "S-4-5",
              "垂直與平行：以具體操作為主。直角是 90 度。直角常用記號。垂直於一線的兩線相互平行。平行線間距離處處相等。作垂直線；作平行線。",
              "垂直與平行",
              "四年級數學 垂直與平行 練習題｜垂直線・平行線・平行線的距離 學習單（附解答）",
              "垂直與平行",
              "國小四年級數學「垂直與平行」免費學習單：找出垂直和平行的直線、四邊形的垂直和平行的邊、垂直和平行的性質與應用題。100題線上練習馬上對答案，附可列印解答。",
              "相交成 90 度是垂直，永不相交是平行",
              "垂直於同一條線的兩條線互相平行。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
