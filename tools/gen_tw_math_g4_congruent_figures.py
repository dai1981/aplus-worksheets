# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：平面圖形的全等（108課綱 S-4-6）
  python3 tools/gen_tw_math_g4_congruent_figures.py
方格上で全等な図形を選ぶ（平移・旋轉・翻轉しても全等）、平移・旋轉・翻轉の見分け、對應邊・對應角、全等図形の周長・面積、性質。
誤答：向きが違うと全等でないと思う、1 マス違う図形を全等とする、對應邊を取り違える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK

R = random.Random(41017)
NM = Names(R)
LET = "甲乙丙丁"
C = 18


def norm(cells):
    mx, my = min(x for x, y in cells), min(y for x, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))


def rot(cells):
    return norm([(-y, x) for x, y in cells])


def flip(cells):
    return norm([(-x, y) for x, y in cells])


def variants(c):
    out = set()
    v = norm(c)
    for _ in range(4):
        out.add(v)
        out.add(flip(v))
        v = rot(v)
    return out


def poly(n):
    cells = {(0, 0)}
    while len(cells) < n:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        cells.add((x + dx, y + dy))
    c = norm(cells)
    if max(x for x, y in c) > 3 or max(y for x, y in c) > 3:
        return None
    return c


def draw(cells, ox, oy, col=FILL):
    return "".join("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (ox + x * C, oy + y * C, C, C, col, GREEN) for x, y in cells)


def grid_bg(w, h):
    s = []
    for i in range(0, w + 1, C):
        s.append("<line x1='%d' y1='0' x2='%d' y2='%d' stroke='#e2e2e2' stroke-width='1'/>" % (i, i, h))
    for j in range(0, h + 1, C):
        s.append("<line x1='0' y1='%d' x2='%d' y2='%d' stroke='#e2e2e2' stroke-width='1'/>" % (j, w, j))
    return "".join(s)


def s1(seen):
    def mk():
        n = R.randint(4, 6)
        base = poly(n)
        if not base or len(variants(base)) < 4:
            return None
        good = R.choice(sorted(variants(base) - {base})) if R.random() < .8 else base
        bads = []
        for _ in range(200):
            b = poly(n + R.choice([0, 0, 1, -1]))
            if b and b not in variants(base) and all(b not in variants(x) for x in bads):
                bads.append(b)
            if len(bads) == 3:
                break
        if len(bads) < 3:
            return None
        opts = bads + [good]
        R.shuffle(opts)
        k = opts.index(good)
        W, H = 5 * C * 5 + 20, 4 * C + 40
        s = grid_bg(W, H) + text(2 * C, 14, "原圖", 13) + draw(base, 4, 22)
        for i, o in enumerate(opts):
            ox = 4 + (i + 1) * (5 * C)
            s += text(ox + 2 * C, 14, LET[i], 14) + draw(o, ox, 22)
        q = "哪一個圖形和原圖<b>全等</b>？（可以轉動或翻面）" + fig(svg_wrap(W, H, s, "原圖和甲乙丙丁"))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s把原圖轉動或翻面後可以完全疊合，形狀和大小都一樣，是全等。其他的格數或形狀不同。" % LET[k])
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def tri():
        a, b, c = sorted(R.sample(range(3, 15), 3))
        if a + b <= c:
            return None
        q = "三角形 ABC 和三角形 DEF 全等，A 對應 D、B 對應 E、C 對應 F。AB ＝ %d 公分，BC ＝ %d 公分，CA ＝ %d 公分。EF 是幾公分？" % (a, b, c)
        return mcq(q, "%d 公分" % b, ["%d 公分" % x for x in (a, c, a + b, b + 1) if x != b], "EF 對應 BC，全等圖形的對應邊相等：%d 公分。" % b)

    def ang():
        x, y = R.randint(30, 100), R.randint(30, 100)
        z = 180 - x - y
        if z < 20:
            return None
        q = "三角形 ABC 和三角形 DEF 全等，A 對應 D、B 對應 E、C 對應 F。∠A ＝ %d 度，∠B ＝ %d 度，∠C ＝ %d 度。∠E 是幾度？" % (x, y, z)
        return mcq(q, "%d 度" % y, ["%d 度" % v for v in (x, z, x + y, 90) if v != y], "∠E 對應 ∠B，全等圖形的對應角相等：%d 度。" % y)

    def rect():
        w, h = R.randint(3, 20), R.randint(2, 15)
        if w == h:
            return None
        q = "兩個長方形全等，第一個長 %d 公分、寬 %d 公分。第二個的周長是幾公分？" % (w, h)
        P = 2 * (w + h)
        return mcq(q, "%d 公分" % P, ["%d 公分" % x for x in (w + h, w * h if w * h != P else P + 2, 4 * w, 2 * P)], "全等圖形大小一樣，周長也一樣：（%d ＋ %d）× 2 ＝ %d（公分）。" % (w, h, P))
    return pick_unique(R, tri, 8, seen) + pick_unique(R, ang, 6, seen) + pick_unique(R, rect, 6, seen)


def s3(seen):
    def mk():
        base = poly(R.randint(4, 5))
        if not base or len(variants(base)) < 8:
            return None
        kind = R.choice(["平移", "旋轉", "翻轉"])
        if kind == "平移":
            new = base
        elif kind == "旋轉":
            new = rot(base) if R.random() < .5 else rot(rot(rot(base)))
            if new == base or new == flip(base):
                return None
        else:
            new = flip(base)
            if new in (base, rot(base), rot(rot(base)), rot(rot(rot(base)))):
                return None
        W, H = 10 * C + 20, 4 * C + 30
        s = grid_bg(W, H) + draw(base, 4, 20) + text(2 * C, 13, "甲", 13) + draw(new, 6 * C, 20) + text(8 * C, 13, "乙", 13)
        q = "甲移動到乙，是用什麼方法？" + fig(svg_wrap(W, H, s, "甲移到乙"))
        e = {"平移": "形狀方向都沒變，只是滑過去，是平移。", "旋轉": "圖形轉了一個角度，是旋轉。", "翻轉": "像照鏡子一樣左右相反，是翻轉。"}[kind]
        return mcq(q, kind, [k for k in ("平移", "旋轉", "翻轉") if k != kind] + ["不是全等"], e + "不論哪一種，甲和乙都全等。")
    return pick_unique(R, mk, 20, seen)


TRUE = ["形狀和大小都一樣的兩個圖形全等。", "全等圖形的對應邊相等。", "全等圖形的對應角相等。", "把圖形翻面後，和原來的圖形全等。",
        "把圖形轉動後，和原來的圖形全等。", "兩個全等的長方形，面積一樣大。"]
FALSE = ["顏色不一樣的兩個圖形一定不全等。", "方向不一樣的兩個圖形一定不全等。", "形狀一樣但大小不一樣的兩個圖形全等。",
         "全等圖形的對應邊不一定相等。", "面積一樣的兩個圖形一定全等。", "兩個正方形一定全等。"]


def s4(seen):
    def mk():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s：%s全等要形狀和大小都一樣，和顏色、方向無關；對應邊、對應角相等。" % (LET[k], ans))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def cut():
        F = [("沿著長方形的一條對角線剪開，得到的兩個三角形怎樣？", "全等", ["不全等", "一個大一個小", "形狀不同"], "兩個三角形可以完全疊合，是全等。"),
             ("把正方形沿著中間的直線剪成兩半，兩個長方形怎樣？", "全等", ["不全等", "一個是正方形", "面積不一樣"], "兩半形狀大小都一樣，是全等。"),
             ("用兩個全等的直角三角形（兩條直角邊一樣長）可以拼出什麼？", "正方形", ["圓形", "五邊形", "梯形（沒有直角）"], "把斜邊對齊拼起來，就是正方形。"),
             ("兩個全等的三角形，其中一個的面積是 12 平方公分，另一個是多少？", "12 平方公分", ["24 平方公分", "6 平方公分", "不一定"], "全等圖形大小一樣，面積也相等。")]
        return mcq(*R.choice(F))

    def area():
        n = R.randint(2, 6)
        a = R.randint(4, 30)
        q = "用 %d 個全等的三角形拼成一個圖形，每個三角形的面積是 %d 平方公分。拼成的圖形面積是多少？" % (n, a)
        return mcq(q, "%d 平方公分" % (n * a), ["%d 平方公分" % x for x in (n + a, a, n * a + a)], "%d 個一樣大的三角形：%d × %d ＝ %d（平方公分）。" % (n, a, n, n * a))

    def side():
        a = R.randint(3, 12)
        b = R.randint(3, 12)
        if a == b:
            return None
        q = "四邊形甲和四邊形乙全等。甲最長的邊是 %d 公分，最短的邊是 %d 公分。乙最長的邊是幾公分？" % (max(a, b) + 2, min(a, b))
        v = max(a, b) + 2
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (min(a, b), v + 2, v * 2)], "全等圖形對應邊相等，乙最長的邊也是 %d 公分。" % v)
    return pick_unique(R, cut, 4, seen) + pick_unique(R, area, 8, seen) + pick_unique(R, side, 8, seen)


def main():
    seen = set()
    sets = [("找出全等的圖形", s1(seen)), ("對應邊和對應角", s2(seen)), ("平移、旋轉、翻轉", s3(seen)),
            ("全等的性質", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["形狀和大小都一樣、可以完全疊合的兩個圖形，叫做<b>全等</b>。",
         "把圖形<b>平移</b>（滑動）、<b>旋轉</b>（轉動）、<b>翻轉</b>（翻面）以後，還是和原來的圖形全等。方向不一樣也可以全等。",
         "全等圖形疊合時，重疊的邊叫<b>對應邊</b>、重疊的角叫<b>對應角</b>：對應邊相等，對應角相等。"],
        [example("三角形 ABC 和 DEF 全等（A→D、B→E、C→F），AB ＝ 5 公分，DE 是多少？", ["DE 對應 AB。", "對應邊相等。"], "5 公分"),
         example("一個圖形翻面後，和原來的全等嗎？", ["翻面後形狀和大小都沒變。"], "全等")],
        [("方向不同就不全等", "轉一轉、翻一翻能疊合，就是全等"),
         ("面積一樣就一定全等", "形狀也要一樣：2 × 6 和 3 × 4 的長方形面積一樣但不全等"),
         ("對應邊找錯", "按照對應的頂點順序找：A→D、B→E，所以 AB 對應 DE")])
    faq = [{"q": "什麼是全等圖形？",
            "a": "形狀和大小都一樣，可以完全疊合的兩個圖形。顏色、位置、方向不同都沒有關係。"},
           {"q": "四年級的全等要學什麼？",
            "a": "108課綱 S-4-6：以操作為主，認識全等圖形，能用平移、旋轉、翻轉做全等疊合，並知道全等圖形的對應角相等、對應邊相等。"},
           {"q": "怎麼判斷兩個圖形全等？",
            "a": "描下其中一個圖形，剪下來在另一個圖形上滑、轉、翻，能完全疊合就是全等。"}]
    make_unit(R, "grade-4", "congruent-figures", "S-4-6",
              "平面圖形的全等：以具體操作為主。形狀大小一樣的兩圖形全等。能用平移、旋轉、翻轉做全等疊合。全等圖形之對應角相等、對應邊相等。",
              "平面圖形的全等",
              "四年級數學 全等圖形 練習題｜平移・旋轉・翻轉・對應邊和對應角 學習單（附解答）",
              "全等圖形",
              "國小四年級數學「全等圖形」免費學習單：找出全等的圖形、平移旋轉翻轉、對應邊和對應角、全等的性質與應用題。100題線上練習馬上對答案，附可列印解答。",
              "形狀和大小都一樣，就是全等",
              "平移、旋轉、翻轉後還是全等；對應邊、對應角相等。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
