# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：幾何形體之操作（平面圖形的分割與重組、展開圖）（108課綱 S-3-4）
  python3 tools/gen_tw_math_g3_nets.py
圖形の分割・組み合わせ、正方體の展開圖（摺れるか・相對的面）、立體の面の数。
展開圖が正方體になるかは、正方體を転がすシミュレーションで判定する（手で決めない）。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK, RED

R = random.Random(31020)
NM = Names(R)
LET = "甲乙丙丁"
C = 26


def roll(cells):
    """展開圖の各マスが正方體のどの面になるか。正方體を転がして、下になる面を記録する"""
    st = set(cells)
    start = cells[0]
    res = {start: "D"}
    stack = [(start, {"U": "U", "D": "D", "N": "N", "S": "S", "E": "E", "W": "W"})]
    while stack:
        (x, y), f = stack.pop()
        for dx, dy, nb in ((1, 0, "E"), (-1, 0, "W"), (0, 1, "S"), (0, -1, "N")):
            c = (x + dx, y + dy)
            if c not in st or c in res:
                continue
            g = dict(f)
            if nb == "E":
                g["D"], g["E"], g["U"], g["W"] = f["E"], f["U"], f["W"], f["D"]
            elif nb == "W":
                g["D"], g["W"], g["U"], g["E"] = f["W"], f["U"], f["E"], f["D"]
            elif nb == "S":
                g["D"], g["S"], g["U"], g["N"] = f["S"], f["U"], f["N"], f["D"]
            else:
                g["D"], g["N"], g["U"], g["S"] = f["N"], f["U"], f["S"], f["D"]
            res[c] = g["D"]
            stack.append((c, g))
    return res


def is_cube_net(cells):
    r = roll(sorted(cells))
    return len(r) == 6 and len(set(r.values())) == 6


OPP = {"U": "D", "D": "U", "N": "S", "S": "N", "E": "W", "W": "E"}


def norm(cells):
    mx, my = min(x for x, y in cells), min(y for x, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))


def rand_hexomino():
    cells = {(0, 0)}
    while len(cells) < 6:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        cells.add((x + dx, y + dy))
    c = norm(cells)
    if max(x for x, y in c) > 4 or max(y for x, y in c) > 3:
        return None
    return c


VALID, INVALID = set(), set()
for _ in range(6000):
    h = rand_hexomino()
    if h:
        (VALID if is_cube_net(h) else INVALID).add(h)
VALID, INVALID = sorted(VALID), sorted(INVALID)
assert len({v for v in VALID}) >= 11


def net_body(cells, ox, oy, labels=None, col=FILL):
    s = []
    for i, (x, y) in enumerate(cells):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (ox + x * C, oy + y * C, C, C, col, GREEN))
        if labels:
            s.append(text(ox + x * C + C / 2, oy + y * C + C / 2 + 6, labels[i], 15))
    return "".join(s)


def four_nets(nets):
    s = []
    for i, n in enumerate(nets):
        ox = 10 + i * 140
        s.append(text(ox + 8, 20, LET[i], 16, anchor="start"))
        s.append(net_body(n, ox, 30))
    return fig(svg_wrap(560, 30 + 4 * C + 14, "".join(s), "甲乙丙丁四個展開圖"))


def s1(seen):
    """平面圖形的分割"""
    CUTS = [("正方形", "沿著一條對角的線剪開", "2 個三角形", ["2 個正方形", "2 個長方形", "1 個三角形和 1 個正方形"], "從一個角剪到對面的角，分成 2 個一樣的三角形。"),
            ("正方形", "從上邊的中間直直剪到下邊的中間", "2 個長方形", ["2 個正方形", "2 個三角形", "4 個長方形"], "直直剪成兩半，每一半都有 4 個直角，是長方形。"),
            ("長方形", "沿著一條對角的線剪開", "2 個三角形", ["2 個長方形", "2 個正方形", "4 個三角形"], "從一個角剪到對面的角，分成 2 個三角形。"),
            ("正方形", "剪兩刀，橫的中間一刀、直的中間一刀", "4 個正方形", ["4 個長方形", "2 個正方形", "4 個三角形"], "橫、直各剪中間一刀，分成 4 個一樣的小正方形。"),
            ("正方形", "沿著兩條對角的線各剪一刀", "4 個三角形", ["2 個三角形", "4 個正方形", "4 個長方形"], "兩條對角的線交叉，分成 4 個三角形。"),
            ("長方形（長是寬的 2 倍）", "從長邊的中間直直剪開", "2 個正方形", ["2 個長方形", "2 個三角形", "4 個正方形"], "長是寬的 2 倍，剪成兩半後，每一塊的長和寬一樣，是正方形。")]
    out = [mcq("一張%s的紙，%s，會得到什麼？" % (a, b), c, d, e) for a, b, c, d, e in CUTS]
    JOIN = [("2 個一樣的直角三角形（直角的兩邊一樣長）", "正方形", ["圓形", "五邊形", "梯形"], "把兩個三角形的斜邊對齊拼起來，就是正方形。"),
            ("2 個一樣的正方形，邊對邊拼在一起", "長方形", ["正方形", "三角形", "圓形"], "兩個正方形並排，長變成 2 倍，是長方形。"),
            ("4 個一樣的小正方形，排成 2 排、每排 2 個", "大正方形", ["長方形", "三角形", "圓形"], "2 排 × 每排 2 個，長和寬一樣，是大正方形。"),
            ("4 個一樣的小正方形，排成 1 排", "長方形", ["正方形", "三角形", "圓形"], "排成 1 排，長是寬的 4 倍，是長方形。")]
    out += [mcq("用%s可以拼成什麼圖形？" % a, b, c, e) for a, b, c, e in JOIN]
    for w in out:
        seen.add(w["q"])

    def count():
        w, h = R.randint(2, 5), R.randint(2, 4)
        if w == h and R.random() < .5:
            return None
        q = "一張長方形的紙，橫的剪 %d 刀、直的剪 %d 刀（每刀都從一邊剪到另一邊），會剪成幾個小長方形？" % (h - 1, w - 1)
        n = w * h
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (w + h - 2, w + h, n + 1, (w - 1) * (h - 1) if (w - 1) * (h - 1) != n else n + 2)],
                   "橫剪 %d 刀分成 %d 排，直剪 %d 刀分成每排 %d 個：%d × %d ＝ %d（個）。" % (h - 1, h, w - 1, w, h, w, n))
    return out + pick_unique(R, count, 10, seen)


def s2(seen):
    """哪一個可以摺成正方體"""
    def mk():
        ok = R.choice(VALID)
        bad = R.sample(INVALID, 3)
        nets = bad + [ok]
        R.shuffle(nets)
        k = nets.index(ok)
        q = "哪一個展開圖可以摺成正方體？" + four_nets(nets)
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s摺起來 6 個面剛好不重疊；其他的摺起來會有兩個面疊在一起，或少了一個面。" % LET[k])

    def no():
        bad = R.choice(INVALID)
        oks = R.sample(VALID, 3)
        nets = oks + [bad]
        R.shuffle(nets)
        k = nets.index(bad)
        q = "哪一個展開圖<b>不能</b>摺成正方體？" + four_nets(nets)
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s摺起來會有兩個面疊在一起（也就會少一個面），不能摺成正方體。" % LET[k])
    return pick_unique(R, mk, 10, seen) + pick_unique(R, no, 10, seen)


def s3(seen):
    """相對的面"""
    def mk():
        net = R.choice(VALID)
        faces = roll(list(net))
        nums = [str(i) for i in range(1, 7)]
        R.shuffle(nums)
        lab = {c: nums[i] for i, c in enumerate(net)}
        a = R.choice(net)
        opp = [c for c in net if faces[c] == OPP[faces[a]]][0]
        adj = [lab[c] for c in net if c not in (a, opp)]
        q = "把這個展開圖摺成正方體，和「%s」相對的面是哪一個？" % lab[a]
        q += fig(svg_wrap(5 * C + 20, 4 * C + 20, net_body(net, 10, 10, [lab[c] for c in net]), "正方體展開圖"))
        return mcq(q, lab[opp], R.sample(adj, 3), "摺起來後，「%s」和「%s」在正方體的兩對面，不會碰在一起；和「%s」相鄰的面都和它碰在一起。" % (lab[a], lab[opp], lab[a]))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    FACTS = [("正方體有幾個面？", "6 個", ["4 個", "8 個", "12 個"], "正方體有上、下、前、後、左、右 6 個面。"),
             ("正方體的每一個面是什麼形狀？", "正方形", ["長方形（不是正方形）", "三角形", "圓形"], "正方體的 6 個面都是一樣大的正方形。"),
             ("正方體的展開圖由幾個正方形組成？", "6 個", ["4 個", "5 個", "8 個"], "正方體有 6 個面，展開後是 6 個正方形。"),
             ("長方體（像牙膏盒）有幾個面？", "6 個", ["4 個", "8 個", "12 個"], "長方體也有上、下、前、後、左、右 6 個面。"),
             ("長方體的展開圖中，相對的兩個面有什麼關係？", "形狀和大小一樣", ["一個大一個小", "一個是三角形", "一定是正方形"], "長方體相對的兩個面一樣大，例如上面和下面。"),
             ("正方體摺起來後，相對的兩個面會怎樣？", "不會碰在一起", ["會疊在一起", "有一條邊碰在一起", "一定是一樣的顏色"], "相對的面在正方體的兩對面，不會碰在一起。"),
             ("不同的展開圖，能不能摺成一樣的正方體？", "可以", ["不可以", "只有一種展開圖", "要看紙的顏色"], "正方體有 11 種不同的展開圖，都能摺成一樣的正方體。"),
             ("把一個紙盒沿著邊剪開攤平，得到的圖叫做什麼？", "展開圖", ["立體圖", "長方形", "平面圖形的周長"], "立體沿著邊剪開攤平，得到的是展開圖。"),
             ("一個正方體的展開圖，摺起來時要黏合的邊和另一條邊有什麼關係？", "一樣長", ["比較長", "比較短", "不一定"], "正方體每一條邊都一樣長，黏合的兩條邊也一樣長。"),
             ("骰子的展開圖中，相對的兩面點數加起來是 7。和 1 點相對的是幾點？", "6 點", ["2 點", "5 點", "3 點"], "1 ＋ 6 ＝ 7，所以和 1 點相對的是 6 點。")]
    out = [mcq(*f) for f in FACTS]
    for w in out:
        seen.add(w["q"])

    def dice():
        a = R.randint(2, 5)
        q = "骰子相對的兩面點數加起來是 7。和 %d 點相對的是幾點？" % a
        return mcq(q, "%d 點" % (7 - a), ["%d 點" % x for x in range(1, 7) if x not in (a, 7 - a)][:3], "%d ＋ %d ＝ 7。" % (a, 7 - a))

    def cubes():
        n = R.randint(2, 9)
        q = "做一個正方體要用 6 個正方形。做 %d 個正方體，一共要用幾個正方形？" % n
        return mcq(q, "%d 個" % (6 * n), ["%d 個" % x for x in (4 * n, 6 + n, 8 * n, 6 * n + 6)], "6 × %d ＝ %d（個）。" % (n, 6 * n))
    return out + pick_unique(R, dice, 4, seen) + pick_unique(R, cubes, 6, seen)


def s5(seen):
    """展開圖缺一個面：補在哪裡"""
    def mk():
        net = list(R.choice(VALID))
        drop = R.choice(net)
        rest = [c for c in net if c != drop]
        # 候補：rest に隣接する空きマス
        cand = set()
        for (x, y) in rest:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c = (x + dx, y + dy)
                if c not in rest and 0 <= c[0] <= 4 and 0 <= c[1] <= 3:
                    cand.add(c)
        good = [c for c in cand if is_cube_net(rest + [c])]
        badc = [c for c in cand if not is_cube_net(rest + [c])]
        if len(good) != 1 or len(badc) < 3:
            return None
        opts = [good[0]] + R.sample(badc, 3)
        R.shuffle(opts)
        k = opts.index(good[0])
        s = net_body(rest, 10, 10)
        for i, (x, y) in enumerate(opts):
            s += "<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (10 + x * C, 10 + y * C, C, C, RED)
            s += text(10 + x * C + C / 2, 10 + y * C + C / 2 + 6, LET[i], 14, col=RED)
        q = "這個展開圖少了一個面。要補在哪一格，才能摺成正方體？" + fig(svg_wrap(5 * C + 20, 4 * C + 20, s, "缺一個面的展開圖"))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "補在%s，摺起來 6 個面剛好不重疊；補在其他格會和已有的面疊在一起。" % LET[k])
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("平面圖形的分割與重組", s1(seen)), ("能不能摺成正方體", s2(seen)), ("相對的面", s3(seen)),
            ("正方體和長方體", s4(seen)), ("補上一個面", s5(seen))]
    cross = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (3, 1))
    demo = fig(svg_wrap(5 * C + 20, 4 * C + 20, net_body(list(cross), 10, 10, ["左", "上", "前", "下", "右", "後"]), "正方體展開圖"))
    body = lesson(
        ["一個圖形可以<b>剪開</b>成幾塊，也可以把幾塊<b>拼</b>成新的圖形。",
         "把正方體沿著邊剪開攤平，得到 6 個正方形連在一起的<b>展開圖</b>。正方體有 11 種展開圖。",
         "排成一直線的 4 個面裡，<b>隔一個</b>的兩個面是相對的面；摺起來時，相對的面不會碰在一起。"],
        [example("這個展開圖摺成正方體後，和「前」相對的是哪一面？" + demo, ["橫排「左、前、右、後」中，隔一個的是相對的面。", "「前」隔一個是「後」。"], "後"),
         example("一張正方形的紙沿著對角的線剪開，得到什麼？", ["從一個角剪到對面的角。"], "2 個三角形")],
        [("6 個正方形連在一起就一定能摺成正方體", "要動手摺一摺：有的會有兩個面疊在一起"),
         ("相鄰的兩個面是相對的面", "相對的面摺起來不會碰在一起"),
         ("正方體只有一種展開圖", "正方體有 11 種展開圖")])
    faq = [{"q": "正方體的展開圖有幾種？",
            "a": "11 種。常見的是「1－4－1」型（中間一排 4 個，上下各 1 個），另外還有「2－3－1」「2－2－2」「3－3」型。"},
           {"q": "三年級的展開圖要學到什麼程度？",
            "a": "108課綱 S-3-4 以操作活動為主：會把平面圖形剪開、重組，初步體驗展開圖怎樣黏合成立體，並知道不同的展開圖可以黏合成同一個立體。"},
           {"q": "怎麼判斷展開圖能不能摺成正方體？",
            "a": "最好的方法是印出來剪一剪、摺一摺。看的時候也可以檢查：摺起來有沒有兩個面疊在一起；一直線上不能超過 4 個面。"}]
    make_unit(R, "grade-3", "nets", "S-3-4",
              "幾何形體之操作：以操作活動為主。平面圖形的分割與重組。初步體驗展開圖如何黏合成立體形體。知道不同之展開圖可能黏合成同一形狀之立體形體。",
              "圖形的分割重組與正方體展開圖",
              "三年級數學 展開圖 練習題｜正方體展開圖・相對的面・圖形剪拼 學習單（附解答）",
              "展開圖與剪拼",
              "國小三年級數學「展開圖」免費學習單：平面圖形的剪開與拼組、哪一個能摺成正方體、相對的面、補上缺少的面。100題線上練習馬上對答案，附可列印解答。",
              "正方體展開圖：6 個正方形，摺起來不重疊",
              "一直線上的 4 個面，隔一個的是相對的面。",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
