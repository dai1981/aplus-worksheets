# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：公分和公尺（108課綱 N-2-11、S-2-3）
  python3 tools/gen_tw_math_g2_centimeters_and_meters.py
尺で長さを讀む（0 から・途中から）、量感（どの單位が合うか）、1 公尺 ＝ 100 公分の換算、長さの加減、線段を描く・比べる。
誤答：途中から測ったのに右端の目盛りを答える、1 公尺 ＝ 10 公分とする、單位をつけ忘れる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81312)
NM = Names(R)


def s1(seen):
    def mk():
        L = R.randint(2, 11)
        q = "鉛筆長幾公分？" + P.ruler(12, 0, L)
        return mcq(q, "%d 公分" % L, ["%d 公分" % x for x in (L + 1, L - 1, L * 10)], "鉛筆的一端對齊 0，另一端到 %d，長 %d 公分。" % (L, L))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, mk2, 10, seen)


def mk2():
    s = R.randint(1, 5)
    L = R.randint(2, 12 - s)
    q = "沒有從 0 開始量。鉛筆長幾公分？" + P.ruler(12, s, L)
    return mcq(q, "%d 公分" % L, ["%d 公分" % x for x in (s + L, L + 1, L - 1 if L > 1 else L + 2) if x != L], "從 %d 量到 %d：%d － %d ＝ %d 公分。也可以數中間有幾個 1 公分。" % (s, s + L, s + L, s, L))


def s2(seen):
    ITEMS = [("一枝鉛筆", "公分", 15), ("一本課本的長", "公分", 26), ("教室門的高", "公尺", 2), ("一根手指的寬", "公分", 1), ("籃球場的長", "公尺", 28),
             ("一張書桌的長", "公分", 60), ("一棵大樹的高", "公尺", 10), ("一個橡皮擦", "公分", 4), ("一間教室的長", "公尺", 9), ("一支湯匙", "公分", 14),
             ("一輛公車的長", "公尺", 12), ("一隻手掌的寬", "公分", 7), ("游泳池的長", "公尺", 25), ("一個杯子的高", "公分", 10), ("一張床的長", "公尺", 2),
             ("一隻螞蟻", "公分", 1), ("學校操場一圈", "公尺", 200), ("一把尺", "公分", 30), ("一條跳繩", "公尺", 2), ("一雙筷子的長", "公分", 24)]
    out = []
    for it, u, v in ITEMS:
        other = "公尺" if u == "公分" else "公分"
        out.append(mcq("%s大約長多少？" % it, "%d %s" % (v, u), ["%d %s" % (v, other), "%d %s" % (v * 10 if v < 50 else v // 10, u), "%d %s" % (v + 100, other)], "%s大約 %d %s。小東西用公分，大東西用公尺。" % (it, v, u)))
    for b in out:
        seen.add(b["q"])
    return out


def s3(seen):
    def mk():
        k = R.choice(["m2cm", "cm2m", "mix"])
        if k == "m2cm":
            m = R.randint(1, 9)
            q = "%d 公尺是幾公分？" % m
            return mcq(q, "%d 公分" % (100 * m), ["%d 公分" % x for x in (10 * m, m, 1000 * m)], "1 公尺 ＝ 100 公分，%d 公尺 ＝ %d 公分。" % (m, 100 * m))
        if k == "cm2m":
            m = R.randint(1, 9)
            q = "%d 公分是幾公尺？" % (100 * m)
            return mcq(q, "%d 公尺" % m, ["%d 公尺" % x for x in (10 * m, 100 * m, m + 1)], "100 公分是 1 公尺，%d 公分是 %d 公尺。" % (100 * m, m))
        m, c = R.randint(1, 5), R.randint(5, 95)
        if c % 10 == 0 and R.random() < .5:
            return None
        if R.random() < .5:
            q = "%d 公尺 %d 公分是幾公分？" % (m, c)
            return mcq(q, "%d 公分" % (100 * m + c), ["%d 公分" % x for x in (m + c, 10 * m + c, 100 * m + c * 10 if 100 * m + 10 * c < 1000 else 100 * m + c + 10)], "%d 公尺 ＝ %d 公分，再加 %d：%d 公分。" % (m, 100 * m, c, 100 * m + c))
        q = "%d 公分是幾公尺幾公分？" % (100 * m + c)
        return mcq(q, "%d 公尺 %d 公分" % (m, c), ["%d 公尺 %d 公分" % (m * 10 + c // 10, c % 10), "%d 公尺 %d 公分" % (m + 1, c), "%d 公尺 %d 公分" % (m, c + 10)], "100 公分 ＝ 1 公尺：%d 公分 ＝ %d 公尺 %d 公分。" % (100 * m + c, m, c))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = R.randint(5, 80), R.randint(5, 80)
        u = R.choice(["公分", "公尺"])
        op = R.choice(["＋", "－"])
        if op == "－" and a <= b:
            a, b = b, a
            if a == b:
                return None
        v = a + b if op == "＋" else a - b
        q = "%d %s %s %d %s ＝ ？" % (a, u, op, b, u)
        other = "公尺" if u == "公分" else "公分"
        return mcq(q, "%d %s" % (v, u), ["%d %s" % (v, other), "%d %s" % (a - b if op == "＋" and a > b else a + b, u), "%d %s" % (v + 10, u)], "單位一樣，直接%s：%d %s。" % ("相加" if op == "＋" else "相減", v, u))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        who, who2 = NM.next(), NM.next()
        k = R.choice(["jump", "ribbon", "tall", "cut"])
        if k == "jump":
            a, b = R.randint(90, 150), R.randint(90, 150)
            if a == b:
                return None
            q = "%s立定跳遠跳了 %d 公分，%s跳了 %d 公分。誰跳得比較遠？遠幾公分？" % (who, a, who2, b)
            w = who if a > b else who2
            d = abs(a - b)
            return mcq(q, "%s，遠 %d 公分" % (w, d), ["%s，遠 %d 公分" % (who2 if w == who else who, d), "%s，遠 %d 公分" % (w, a + b), "%s，遠 %d 公尺" % (w, d)], "%d － %d ＝ %d 公分。" % (max(a, b), min(a, b), d))
        if k == "ribbon":
            a, b = R.randint(20, 60), R.randint(20, 60)
            q = "一條緞帶長 %d 公分，另一條長 %d 公分，接起來（不重疊）一共長幾公分？" % (a, b)
            return mcq(q, "%d 公分" % (a + b), ["%d 公分" % x for x in (abs(a - b) if a != b else a, a + b + 10, a + b - 1)], "%d ＋ %d ＝ %d。" % (a, b, a + b))
        if k == "tall":
            h = R.randint(115, 135)
            g = R.randint(3, 15)
            q = "%s身高 %d 公分，一年後長高了 %d 公分。現在身高是幾公尺幾公分？" % (who, h, g)
            v = h + g
            return mcq(q, "1 公尺 %d 公分" % (v - 100), ["%d 公尺 %d 公分" % (v // 10, v % 10), "1 公尺 %d 公分" % (h - 100), "1 公尺 %d 公分" % (v - 100 + 10)], "%d ＋ %d ＝ %d 公分 ＝ 1 公尺 %d 公分。" % (h, g, v, v - 100))
        L = R.randint(2, 9)
        c = R.randint(20, 80)
        q = "一條 %d 公尺長的繩子，剪掉 %d 公分，還剩幾公分？" % (L, c)
        v = 100 * L - c
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (L - c if L > c else c - L, 10 * L - c if 10 * L > c else v + 10, v + 10)], "%d 公尺 ＝ %d 公分，%d － %d ＝ %d。" % (L, 100 * L, 100 * L, c, v))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("用尺量長度", s1(seen)), ("用公分還是公尺", s2(seen)), ("公尺和公分的換算", s3(seen)),
            ("長度的加減", s4(seen)), ("長度的應用問題", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["用尺量：<b>一端對齊 0</b>，看另一端對到幾，就是幾公分。" + P.ruler(10, 0, 6),
         "沒有從 0 開始時，用「右邊的刻度 － 左邊的刻度」。",
         "<b>1 公尺 ＝ 100 公分</b>。小東西用公分，大東西用公尺。"],
        [example("鉛筆從 2 量到 9", ["9 － 2。"], "7 公分"),
         example("2 公尺 35 公分是幾公分？", ["2 公尺 ＝ 200 公分。", "200 ＋ 35。"], "235 公分")],
        [("從 2 量到 9，說是 9 公分", "要減掉開始的 2：7 公分"),
         ("1 公尺 ＝ 10 公分", "1 公尺 ＝ 100 公分"),
         ("教室門高 2 公分", "大東西用公尺：2 公尺")])
    faq = [{"q": "二年級要學哪些長度單位？",
            "a": "108課綱 N-2-11：公分和公尺，包含實測、量感、估測、計算和單位換算；S-2-3 用直尺測量長度、畫線段。"},
           {"q": "孩子量長度常錯在哪？",
            "a": "最常見的是沒有對齊 0，或從 1 開始量。可以先練「對齊 0」，再練從中間量的「右減左」。"},
           {"q": "怎麼培養量感？",
            "a": "記住幾個身邊的長度：手指寬約 1 公分、手掌寬約 7 公分、大人一步約 60 公分、教室門高約 2 公尺。"}]
    make_unit(R, "grade-2", "centimeters-and-meters", "N-2-11",
              "長度：「公分」、「公尺」。實測、量感、估測與計算。單位換算。",
              "公分和公尺：用尺量長度",
              "二年級數學 公分公尺 練習題｜用尺量長度・單位換算 學習單（附解答）",
              "公分和公尺",
              "國小二年級數學「公分和公尺」免費學習單：用尺量長度（從 0 和不從 0）、用公分還是公尺、1 公尺＝100 公分的換算、長度加減、跳遠和緞帶應用題。100題線上練習，圖多，附可列印解答。",
              "1 公尺 ＝ 100 公分",
              "量長度一端對齊 0；不從 0 開始就用右減左。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
