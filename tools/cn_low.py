# -*- coding: utf-8 -*-
"""
中国 小学低年级（一・二年级）の自前の問題：位置、10以内の数、分与合、立体图形、11~20、钟表（整时・半时）、人民币、找规律。
k_pics の絵を中国語の aria-label で使う。setup(R) してから使う。
"""
import math
import random
import k_pics as K
from f_common import pattern_svg
from ws_common import svg_wrap, text, fig, INK, GREEN, RED, FILL
from cn_common import mcq, Names

R = random.Random(0)
NM = Names(R)


def setup(rnd):
    global R, NM
    R = rnd
    NM = Names(rnd)


KIND = {"apple": ("苹果", "个"), "star": ("星星", "颗"), "ball": ("皮球", "个"), "button": ("纽扣", "颗"),
        "fish": ("小鱼", "条"), "flower": ("花", "朵"), "heart": ("爱心", "个"), "duck": ("小鸭", "只"),
        "cup": ("杯子", "个"), "bug": ("瓢虫", "只")}
KINDS = list(KIND)
LET = "ABCD"
ORD = ["", "第1", "第2", "第3", "第4", "第5", "第6", "第7", "第8", "第9", "第10"]


def nm(k):
    return KIND[k][0]


def cl(k):
    return KIND[k][1]


def zh(svg, label):
    import re
    return fig(re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1))


def row(n, k):
    return zh(K.row_svg(n, k, 10), "%d%s%s" % (n, cl(k), nm(k)))


def scatter(n, k):
    return zh(K.scatter_svg(n, k, R.randint(1, 10 ** 6)), nm(k))


def near(v, lo=0, hi=None, ds=(1, -1, 2, -2, 10, -10, 3)):
    return [v + d for d in ds if v + d >= lo and (hi is None or v + d <= hi) and v + d != v]


# ------------------------------------------------------------------ 位置（上下、前后、左右）
def pos_table():
    W = {"above": "上面", "below": "下面", "beside": "旁边", "beside-left": "旁边"}

    def mk():
        k = R.choice(KINDS)
        rel = R.choice(list(W))
        pic = zh(K.table_scene_svg(k, rel), "桌子和%s" % nm(k))
        return mcq("%s在桌子的哪里？%s" % (nm(k), pic), "桌子%s" % W[rel],
                   ["桌子%s" % w for w in ("上面", "下面", "旁边", "里面") if w != W[rel]],
                   "看桌面：%s在桌子的<b>%s</b>。" % (nm(k), W[rel]))
    return mk


def pos_box():
    W = {"front": "前面", "behind": "后面", "beside": "旁边", "above": "上面"}
    TIP = {"front": "它挡在箱子前，看得见全部。", "behind": "它被箱子挡住了一部分。", "beside": "它和箱子并排放在地上。", "above": "它比箱子高。"}

    def mk():
        k = R.choice(KINDS)
        rel = R.choice(list(W))
        pic = zh(K.box_scene_svg(k, rel), "箱子和%s" % nm(k))
        return mcq("%s在箱子的哪里？%s" % (nm(k), pic), "箱子%s" % W[rel],
                   ["箱子%s" % w for w in ("前面", "后面", "旁边", "上面") if w != W[rel]],
                   "%s所以在<b>箱子%s</b>。" % (TIP[rel], W[rel]))
    return mk


def pos_shelf(kinds=("top", "ord", "near")):
    def mk():
        L = R.randint(4, 5)
        ks = R.sample(KINDS, L)
        pic = zh(K.shelf_svg(ks), "%d层的书架" % L)
        how = R.choice(kinds)
        if how == "top":
            up = R.random() < 0.5
            a = ks[0] if up else ks[-1]
            q = "书架的最%s层放的是什么？" % ("上" if up else "下")
            e = "看最%s面的一层，是<b>%s</b>。" % ("上" if up else "下", nm(a))
            w = [nm(ks[-1] if up else ks[0]), nm(ks[1] if up else ks[-2]), nm(ks[2])]
        elif how == "ord":
            up = R.random() < 0.5
            p = R.randint(2, L - 1)
            a = ks[p - 1] if up else ks[L - p]
            q = "从%s往%s数，第%d层放的是什么？" % ("上" if up else "下", "下" if up else "上", p)
            e = "从%s面数起：第1层、第2层……第%d层是<b>%s</b>。" % ("上" if up else "下", p, nm(a))
            w = [nm(ks[L - p] if up else ks[p - 1]), nm(ks[p] if up else ks[L - p - 1]), nm(ks[p - 2] if up else ks[L - p + 1])]
        else:
            i = R.randint(1, L - 2)
            up = R.random() < 0.5
            a = ks[i - 1] if up else ks[i + 1]
            q = "%s的上一层放的是什么？" % nm(ks[i]) if up else "%s的下一层放的是什么？" % nm(ks[i])
            e = "从%s那层往%s一层，是<b>%s</b>。" % (nm(ks[i]), "上" if up else "下", nm(a))
            w = [nm(ks[i + 1] if up else ks[i - 1]), nm(ks[i]), nm(ks[(i + 2) % L])]
        return mcq(q + pic, nm(a), w + [nm(k) for k in ks], e)
    return mk


def pos_lr():
    def mk():
        ks = R.sample(KINDS, 5)
        pic = zh(K.kinds_row_svg(ks), "一排东西")
        how = R.choice(["right", "left", "between", "end", "ord"])
        if how in ("right", "left"):
            i = R.randint(1, 3)
            a = ks[i + 1] if how == "right" else ks[i - 1]
            q = "%s的%s边紧挨着的是什么？" % (nm(ks[i]), "右" if how == "right" else "左")
            w = [nm(ks[i - 1] if how == "right" else ks[i + 1]), nm(ks[i])]
            e = "从%s往%s看一个，是<b>%s</b>。" % (nm(ks[i]), "右" if how == "right" else "左", nm(a))
        elif how == "between":
            i = R.randint(0, 2)
            a = ks[i + 1]
            q = "%s和%s中间的是什么？" % (nm(ks[i]), nm(ks[i + 2]))
            w = [nm(ks[i]), nm(ks[i + 2]), nm(ks[(i + 3) % 5])]
            e = "%s和%s的中间是<b>%s</b>。" % (nm(ks[i]), nm(ks[i + 2]), nm(a))
        elif how == "end":
            left = R.random() < 0.5
            a = ks[0] if left else ks[-1]
            q = "最%s边的是什么？" % ("左" if left else "右")
            w = [nm(ks[-1] if left else ks[0]), nm(ks[1] if left else ks[-2]), nm(ks[2])]
            e = "看最%s边，是<b>%s</b>。" % ("左" if left else "右", nm(a))
        else:
            left = R.random() < 0.5
            p = R.randint(2, 4)
            a = ks[p - 1] if left else ks[5 - p]
            q = "从%s往%s数，第%d个是什么？" % ("左" if left else "右", "右" if left else "左", p)
            w = [nm(ks[5 - p] if left else ks[p - 1]), nm(ks[p] if left else ks[4 - p]), nm(ks[p - 2] if left else ks[6 - p] if 6 - p < 5 else ks[0])]
            e = "从%s边数起，第%d个是<b>%s</b>。" % ("左" if left else "右", p, nm(a))
        return mcq(q + pic, nm(a), w + [nm(k) for k in ks], e)
    return mk


def grid_svg(ks):
    sp = 62
    s = []
    for r in range(4):
        s.append("<line x1='8' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (8 + r * sp, 8 + 3 * sp, 8 + r * sp, GREEN))
        s.append("<line x1='%d' y1='8' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (8 + r * sp, 8 + r * sp, 8 + 3 * sp, GREEN))
    for i, k in enumerate(ks):
        s.append(K.obj(k, 8 + sp / 2 + (i % 3) * sp, 8 + sp / 2 + (i // 3) * sp, 18))
    return zh(svg_wrap(16 + 3 * sp, 16 + 3 * sp, "".join(s), "x"), "九格里的东西")


def pos_grid():
    D = {"上面": (-1, 0), "下面": (1, 0), "左边": (0, -1), "右边": (0, 1)}

    def mk():
        ks = R.sample(KINDS, 9)
        r, c = R.randint(0, 2), R.randint(0, 2)
        dirs = [d for d, (dr, dc) in D.items() if 0 <= r + dr <= 2 and 0 <= c + dc <= 2]
        d = R.choice(dirs)
        a = ks[(r + D[d][0]) * 3 + c + D[d][1]]
        w = [nm(ks[(r + D[x][0]) * 3 + c + D[x][1]]) for x in dirs if x != d] + [nm(ks[r * 3 + c])]
        return mcq("%s%s紧挨着的是什么？%s" % (nm(ks[r * 3 + c]), d, grid_svg(ks)), nm(a), w + [nm(k) for k in ks],
                   "从%s那一格往%s走一格，是<b>%s</b>。" % (nm(ks[r * 3 + c]), d[0], nm(a)))
    return mk


def pos_words():
    P = [("上", "下"), ("下", "上"), ("前", "后"), ("后", "前"), ("左", "右"), ("右", "左")]
    pool = P[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        a, b = pool.pop()
        return mcq("和“%s”相对的方向是什么？" % a, b, [x for x in "上下前后左右" if x not in (a, b)],
                   "“%s”和“%s”是一对，方向正好相反。<b>%s</b>" % (a, b, b))
    return mk


def pos_lr_body():
    """面对面时左右相反"""
    S = [("你用哪只手写字？大多数人用右手。右手在身体的哪一边？", "右边", ["左边", "前边", "后边"], "写字的手（大多数人）是右手，在身体的<b>右边</b>。"),
         ("小明和你面对面站着，他举起右手。从你这边看，他举的手在你的哪一边？", "左边", ["右边", "上边", "后边"], "面对面时，对方的右手在你的<b>左边</b>。"),
         ("上下楼梯时要靠右走。你上楼时靠哪边的扶手？", "右边的扶手", ["左边的扶手", "中间", "哪边都可以"], "靠右走，就扶<b>右边的扶手</b>。"),
         ("排队时，小红前面有 3 人，后面有 2 人。这一队一共有几人？", "6 人", ["5 人", "3 人", "2 人"], "前面 3 人 ＋ 小红 1 人 ＋ 后面 2 人 ＝ <b>6 人</b>。"),
         ("排队时，乐乐前面有 4 人，后面有 4 人。这一队一共有几人？", "9 人", ["8 人", "4 人", "5 人"], "4 ＋ 1 ＋ 4 ＝ <b>9 人</b>，别忘了乐乐自己。"),
         ("小华从左往右数是第 3 个，从右往左数是第 5 个。这一排一共有几个小朋友？", "7 个", ["8 个", "5 个", "3 个"], "3 ＋ 5 － 1 ＝ <b>7 个</b>，小华被数了两次。")]
    pool = S[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a, w, e = pool.pop()
        return mcq(q, a, w, e)
    return mk


# ------------------------------------------------------------------ 10 以内的数
def count_pic(lo, hi):
    def mk():
        n, k = R.randint(lo, hi), R.choice(KINDS)
        pic = scatter(n, k) if n <= 12 and R.random() < 0.6 else row(n, k)
        return mcq("有几%s%s？%s" % (cl(k), nm(k), pic), "%d%s" % (n, cl(k)), ["%d%s" % (x, cl(k)) for x in near(n, 1)],
                   "一个一个地数，不重复、不遗漏，一共 <b>%d%s</b>。" % (n, cl(k)))
    return mk


def tf_count():
    TF = ["dot", "apple", "star", "flower", "ball"]

    def mk():
        n, k = R.randint(1, 10), R.choice(TF)
        u = "朵" if k == "flower" else "个"
        return mcq("十格图里有几%s？%s" % (u, zh(K.tenframe_svg(n, 1, k), "十格图")), "%d%s" % (n, u),
                   ["%d%s" % (x, u) for x in near(n, 0, 10) + [10 - n]],
                   "一行 5 格。%s<b>%d%s</b>。" % ("5 和 %d 合起来是 " % (n - 5) if n > 5 else "数一数是 ", n, u))
    return mk


def cmp_sym(lo, hi):
    def mk():
        a, b = R.randint(lo, hi), R.randint(lo, hi)
        ok = ">" if a > b else "<" if a < b else "="
        return mcq("%d ○ %d，○ 里填什么？" % (a, b), ok, [x for x in (">", "<", "=", "＋") if x != ok],
                   "%d 比 %d %s，所以填 <b>%s</b>。" % (a, b, "大" if a > b else "小" if a < b else "一样大", ok))
    return mk


def cmp_more(lo, hi):
    def mk():
        ka, kb = R.sample(KINDS, 2)
        a, b = R.sample(range(lo, hi + 1), 2)
        pic = zh(K.match_svg([(a, ka, "", None), (b, kb, "", None)]), "两行东西")
        big = ka if a > b else kb
        small = kb if a > b else ka
        return mcq("%s和%s，哪种多？%s" % (nm(ka), nm(kb), pic), "%s多" % nm(big),
                   ["%s多" % nm(small), "一样多", "不能比"],
                   "一个对一个地比，%s有剩下的，所以<b>%s多</b>。" % (nm(big), nm(big)))
    return mk


def ord_vs_count():
    def mk():
        n, k = R.randint(5, 9), R.choice(KINDS)
        p = R.randint(2, n - 1)
        if R.random() < 0.5:
            q = "一排有 %d%s%s。从左数，第 %d %s涂上颜色，涂了几%s？" % (n, cl(k), nm(k), p, cl(k), cl(k))
            return mcq(q, "1%s" % cl(k), ["%d%s" % (x, cl(k)) for x in (p, p - 1, n - p, n)],
                       "“第 %d %s”只是一%s，所以涂了 <b>1%s</b>。" % (p, cl(k), cl(k), cl(k)))
        q = "一排有 %d%s%s。从左数，把 %d%s涂上颜色，没涂的有几%s？" % (n, cl(k), nm(k), p, cl(k), cl(k))
        return mcq(q, "%d%s" % (n - p, cl(k)), ["%d%s" % (x, cl(k)) for x in (n - p + 1, p, n, 1)],
                   "%d%s涂了 %d%s，还剩 <b>%d%s</b>。" % (n, cl(k), p, cl(k), n - p, cl(k)))
    return mk


def ord_row():
    def mk():
        L = R.randint(6, 9)
        ks = R.sample(KINDS, L)
        left = R.random() < 0.6
        p = R.randint(1, L - 1)
        idx = p - 1 if left else L - p
        a = nm(ks[idx])
        w = [nm(ks[L - p]) if left else nm(ks[p - 1]), nm(ks[idx - 1]) if idx > 0 else None, nm(ks[idx + 1]) if idx + 1 < L else None, nm(ks[(idx + 2) % L])]
        return mcq("从%s边数，第 %d 个是什么？%s" % ("左" if left else "右", p, zh(K.kinds_row_svg(ks), "一排东西")), a, w,
                   "从%s边开始，第1、第2……数到第 %d 个是<b>%s</b>。" % ("左" if left else "右", p, a))
    return mk


def seq_fill(lo, hi, step=1):
    def mk():
        down = R.random() < 0.3
        L = 5
        st = R.randint(lo, hi - step * (L - 1))
        sq = list(range(st, st + step * L, step))
        if down:
            sq = sq[::-1]
        p = R.randint(1, L - 1)
        ans = sq[p]
        shown = ["?" if i == p else x for i, x in enumerate(sq)]
        return mcq("按顺序排一排，? 是几？%s" % zh(K.cards_svg([str(x) for x in shown]), "数字卡片"), str(ans),
                   [str(x) for x in (ans + 1, ans - 1, ans + 2 * (-step if down else step), sq[p - 1]) if x >= 0],
                   "这些数一个比一个%s %d，%d 后面是 <b>%d</b>。" % ("小" if down else "大", step, sq[p - 1], ans))
    return mk


def before_after(lo, hi):
    def mk():
        n = R.randint(lo + 1, hi - 1)
        up = R.random() < 0.5
        a = n + 1 if up else n - 1
        return mcq("和 %d 相邻，比 %d %s 1 的数是几？" % (n, n, "大" if up else "小"), str(a), [str(x) for x in (n - 1 if up else n + 1, n, a + 1, a - 1) if x >= 0],
                   "按顺序数，%d %s面的数是 <b>%d</b>。" % (n, "后" if up else "前", a))
    return mk


def bond(hi):
    def mk():
        w = R.randint(2, hi)
        a = R.randint(1, w - 1)
        pic = zh(K.bond_svg(w, a, "?"), "分与合")
        if R.random() < 0.5:
            return mcq("%d 可以分成 %d 和几？%s" % (w, a, pic), str(w - a), [str(x) for x in near(w - a, 0, hi) + [w]],
                       "%d 和 %d 合成 %d，所以 %d 可以分成 %d 和 <b>%d</b>。" % (a, w - a, w, w, a, w - a))
        return mcq("%d 和 %d 合成几？%s" % (a, w - a, zh(K.bond_svg("?", a, w - a), "分与合")), str(w), [str(x) for x in near(w, 1, hi + 2) + [abs(2 * a - w)]],
                   "%d 和 %d 合起来是 <b>%d</b>。" % (a, w - a, w))
    return mk


def bond_ways():
    def mk():
        w = R.randint(3, 10)
        a = R.randint(1, w - 1)
        ok = "%d 和 %d" % (a, w - a)
        bad = ["%d 和 %d" % (a, w - a + d) for d in (1, -1, 2, -2) if w - a + d > 0]
        return mcq("哪一组数能合成 %d？（%s开头）" % (w, a), ok, bad,
                   "%d ＋ %d ＝ %d，所以是 <b>%s</b>。" % (a, w - a, w, ok))
    return mk


def bond_count():
    def mk():
        w = R.randint(3, 10)
        n = w - 1
        return mcq("把 %d 分成两个数（每个数都不是 0），一共有几种分法？" % w, "%d 种" % n, ["%d 种" % x for x in (n + 1, n - 1, w, w // 2) if x > 0],
                   "1 和 %d、2 和 %d……%d 和 1，一共 <b>%d 种</b>。" % (w - 1, w - 2, w - 1, n))
    return mk


# ------------------------------------------------------------------ 立体图形
SOL = {"cuboid": "长方体", "cube": "正方体", "cylinder": "圆柱", "sphere": "球"}
OBJ = [("魔方", "cube"), ("骰子", "cube"), ("牙膏盒", "cuboid"), ("鞋盒", "cuboid"), ("字典", "cuboid"), ("冰箱", "cuboid"), ("易拉罐", "cylinder"),
       ("茶叶筒", "cylinder"), ("铅笔（没削的）", "cylinder"), ("卷纸", "cylinder"), ("乒乓球", "sphere"), ("篮球", "sphere"), ("西瓜", "sphere"),
       ("地球仪", "sphere"), ("积木方块", "cube"), ("砖", "cuboid"), ("饼干筒", "cylinder"), ("橙子", "sphere"), ("粉笔盒", "cuboid"), ("玻璃珠", "sphere"), ("纸巾盒", "cuboid"), ("水桶（没把手）", "cylinder")]


def cuboid_svg(w, h, d, col="#7fb3e6"):
    x0, y0 = 10, 10 + d * 0.5
    s = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + w, y0, x0 + w, y0 + h, x0, y0 + h, col, INK),
         "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#b9d6f2' stroke='%s' stroke-width='2'/>" % (x0, y0, x0 + d * 0.7, y0 - d * 0.5, x0 + w + d * 0.7, y0 - d * 0.5, x0 + w, y0, INK),
         "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#4f86bd' stroke='%s' stroke-width='2'/>" % (x0 + w, y0, x0 + w + d * 0.7, y0 - d * 0.5, x0 + w + d * 0.7, y0 + h - d * 0.5, x0 + w, y0 + h, INK)]
    return svg_wrap(int(x0 + w + d * 0.7 + 10), int(y0 + h + 10), "".join(s), "立体图形")


def solid_pic(kind, col):
    if kind == "cuboid":
        return zh(cuboid_svg(R.choice([70, 80, 90, 100, 110]), R.choice([35, 40, 45, 50]), R.choice([30, 40, 50])), "立体图形")
    return zh(K.one_solid_svg(kind, col, R.choice([32, 36, 40, 44])), "立体图形")


def sol_name():
    def mk():
        k = R.choice(list(SOL))
        col = R.choice(["red", "blue", "yellow", "green"])
        return mcq("这是什么图形？%s" % solid_pic(k, col), SOL[k], [SOL[x] for x in SOL if x != k] + ["圆锥"],
                   "%s<b>%s</b>。" % ({"cuboid": "6 个面都是长方形（或有 2 个正方形），长长的，是", "cube": "6 个面都是一样大的正方形，是",
                                       "cylinder": "上下两个面是一样大的圆，能滚动，是", "sphere": "圆圆的，从哪边看都一样，是"}[k], SOL[k]))
    return mk


def sol_obj():
    pool = OBJ[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        o, k = pool.pop()
        return mcq("“%s”的形状最像哪种立体图形？" % o, SOL[k], [SOL[x] for x in SOL if x != k],
                   "%s的形状像<b>%s</b>。" % (o, SOL[k]))
    return mk


SOLF = [("哪种图形最容易滚动，往哪边都能滚？", "球", ["正方体", "长方体", "圆柱"]),
        ("哪种图形放倒了能滚，立起来又能放稳？", "圆柱", ["球", "正方体", "长方体"]),
        ("哪种图形的 6 个面都是一样大的正方形？", "正方体", ["长方体", "圆柱", "球"]),
        ("哪种图形一个平平的面也没有？", "球", ["圆柱", "正方体", "长方体"]),
        ("哪种图形有 2 个平平的圆面？", "圆柱", ["球", "正方体", "长方体"]),
        ("搭高楼时，哪一种积木最难放在最下面？", "球", ["正方体", "长方体", "圆柱（立着放）"]),
        ("把正方体的一个面印在纸上，会得到什么形状？", "正方形", ["圆", "三角形", "长方形"]),
        ("把圆柱的底面印在纸上，会得到什么形状？", "圆", ["正方形", "三角形", "长方形"]),
        ("把长方体最大的一个面印在纸上，通常得到什么形状？", "长方形", ["圆", "三角形", "球"]),
        ("正方体有几个面？", "6 个", ["4 个", "8 个", "12 个"]),
        ("长方体有几个面？", "6 个", ["4 个", "8 个", "2 个"])]


def sol_fact():
    pool = SOLF[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a, w = pool.pop()
        return mcq(q, a, w, "答案是<b>%s</b>。" % a)
    return mk


def sol_count():
    def mk():
        items = [R.choice(list(SOL)) for _ in range(R.randint(5, 8))]
        k = R.choice(items)
        n = items.count(k)
        W, sp = 70 * len(items) + 10, 70
        s = []
        for i, it in enumerate(items):
            if it == "cuboid":
                x0 = 10 + i * sp
                s.append("<g transform='translate(%d 14) scale(0.55)'>%s</g>" % (x0, cuboid_svg(80, 45, 40).split(">", 1)[1].rsplit("</svg>", 1)[0]))
            else:
                s.append(K.solid(it, 10 + i * sp + 30, 46, 24, R.choice(["red", "blue", "yellow", "green"])))
        pic = zh(svg_wrap(W, 90, "".join(s), "x"), "一排立体图形")
        return mcq("下面有几个%s？%s" % (SOL[k], pic), "%d 个" % n, ["%d 个" % x for x in near(n, 0, 8) + [len(items)]],
                   "只数%s，一共 <b>%d 个</b>。" % (SOL[k], n))
    return mk


# ------------------------------------------------------------------ 11~20
def teen_rods():
    def mk():
        o = R.randint(1, 9)
        n = 10 + o
        if R.random() < 0.5:
            return mcq("一捆是 10 根。图上一共有几根小棒？%s" % zh(K.rods_svg(1, o), "1捆和%d根" % o), "%d 根" % n,
                       ["%d 根" % x for x in (o, o * 10 + 1, n + 1, n - 1)], "1 捆是 10 根，再加 %d 根，是 <b>%d 根</b>。" % (o, n))
        return mcq("1 个十和 %d 个一合起来是几？" % o, str(n), [str(x) for x in (o, 10 * o + 1, n + 1, n - 1)],
                   "1 个十是 10，再加 %d 个一，是 <b>%d</b>。" % (o, n))
    return mk


def teen_place():
    def mk():
        n = R.randint(11, 20)
        t, o = n // 10, n % 10
        if R.random() < 0.5:
            return mcq("%d 的十位上是几，个位上是几？" % n, "十位 %d，个位 %d" % (t, o),
                       ["十位 %d，个位 %d" % (o, t), "十位 %d，个位 %d" % (t, o + 1), "十位 %d，个位 %d" % (t + 1, o)],
                       "%d 是 %d 个十和 %d 个一：<b>十位 %d，个位 %d</b>。" % (n, t, o, t, o))
        return mcq("%d 里面有几个十和几个一？" % n, "%d 个十和 %d 个一" % (t, o),
                   ["%d 个十和 %d 个一" % (o, t) if o else "0 个十和 %d 个一" % n, "%d 个十和 %d 个一" % (t, o + 1), "%d 个一" % t],
                   "<b>%d 个十和 %d 个一</b>。" % (t, o))
    return mk


def teen_calc():
    def mk():
        o = R.randint(1, 9)
        how = R.choice(["10+", "-o", "-10"])
        if how == "10+":
            return mcq("10 ＋ %d ＝ ？" % o, str(10 + o), [str(x) for x in (o, 11 + o, 9 + o, 100 + o)], "10 和 %d 合成 <b>%d</b>。" % (o, 10 + o))
        if how == "-o":
            return mcq("%d － %d ＝ ？" % (10 + o, o), "10", [str(x) for x in (o, 10 + o, 9, 11)], "去掉个位上的 %d，剩下 <b>10</b>。" % o)
        return mcq("%d － 10 ＝ ？" % (10 + o), str(o), [str(x) for x in (10, 10 + o, o + 1, 1)], "去掉 1 个十，剩下 <b>%d</b>。" % o)
    return mk


# ------------------------------------------------------------------ 钟表
def clock_svg(h, m, size=170):
    cx = cy = size / 2.0
    Rr = cx - 6
    k = Rr / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, Rr, GREEN, 5 * k)]
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = Rr - (13 if i % 5 == 0 else 7) * k
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f'/>" % (
            cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + (Rr - 3 * k) * math.cos(a), cy + (Rr - 3 * k) * math.sin(a), INK, (2.6 if i % 5 == 0 else 1.1) * k))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>" % (cx, cy, cx + Rr * 0.5 * math.cos(ah), cy + Rr * 0.5 * math.sin(ah), INK, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>" % (cx, cy, cx + Rr * 0.84 * math.cos(am), cy + Rr * 0.84 * math.sin(am), RED, 4.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append(text(cx + (Rr - 29 * k) * math.cos(a), cy + (Rr - 29 * k) * math.sin(a) + 7 * k, str(n), 19 * k))
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, INK))
    return fig(svg_wrap(int(size), int(size), "".join(s), "钟面 %d时%d分" % (h, m)))


def t_read(half=False):
    def mk():
        h = R.randint(1, 12)
        m = 30 if half and R.random() < 0.6 else 0
        ok = "%d 时%s" % (h, " 30 分" if m else "")
        nxt = h % 12 + 1
        w = ["%d 时%s" % (nxt, " 30 分" if m else ""), "%d 时" % (6 if h == 12 else 12) if not m else "%d 时" % h, "%d 时%s" % (h if not m else nxt, "" if m else " 30 分")]
        if m == 0:
            w.append("%d 时" % (h % 12 + 2 if h < 11 else 1))
        e = ("分针指着 12，时针指着 %d，是 <b>%d 时</b>。" % (h, h) if not m else
             "分针指着 6 是 30 分；时针在 %d 和 %d 中间，已经过了 %d，是 <b>%d 时 30 分</b>。" % (h, nxt, h, h))
        return mcq("钟面上是几时%s？%s" % ("几分" if half else "", clock_svg(h, m)), ok, w, e)
    return mk


def t_digital():
    def mk():
        h = R.randint(1, 12)
        m = R.choice([0, 30]) if R.random() < 0.6 else 0
        ok = "%d:%02d" % (h, m)
        return mcq("钟面上的时间用电子表怎么表示？%s" % clock_svg(h, m), ok,
                   ["%d:%02d" % (h % 12 + 1, m), "%d:%02d" % (h, 30 if m == 0 else 0), "%d:%02d" % (12 if m == 0 else 6, h)],
                   "%d 时%s写成 <b>%s</b>。" % (h, " 30 分" if m else "", ok))
    return mk


def t_hands():
    def mk():
        h = R.randint(1, 12)
        if R.random() < 0.5:
            return mcq("%d 时整，分针指着几？" % h, "12", ["%d" % h, "6", "%d" % (h % 12 + 1)] if h not in (6, 12) else ["6" if h == 12 else "1", "3", "9"],
                       "整时的时候，分针都指着 <b>12</b>，时针指着 %d。" % h)
        return mcq("%d 时整，时针指着几？" % h, str(h), [str(x) for x in (12 if h != 12 else 6, h % 12 + 1, (h + 10) % 12 + 1)],
                   "整时的时候，时针指着 <b>%d</b>，分针指着 12。" % h)
    return mk


def t_about():
    def mk():
        h = R.randint(1, 12)
        before = R.random() < 0.5
        m = R.choice([50, 55]) if before else R.choice([5, 10])
        hh = (h - 1 - 1) % 12 + 1 if before else h
        ok = "快 %d 时了" % h if before else "刚过 %d 时" % h
        return mcq("钟面上大约是几时？%s" % clock_svg(hh, m), ok,
                   ["刚过 %d 时" % h if before else "快 %d 时了" % h, "%d 时 30 分" % h, "快 %d 时了" % (h % 12 + 1) if before else "刚过 %d 时" % ((h - 2) % 12 + 1)],
                   "分针%s 12，所以是<b>%s</b>。" % ("快到" if before else "刚走过", ok))
    return mk


def t_life():
    S = [("早上起床", 7, "上午"), ("上第一节课", 8, "上午"), ("吃午饭", 12, "中午"), ("放学回家", 4, "下午"), ("吃晚饭", 6, "晚上"), ("晚上睡觉", 9, "晚上"),
         ("做早操", 9, "上午"), ("看动画片", 5, "下午"), ("吃早饭", 7, "上午"), ("洗澡", 8, "晚上")]

    def mk():
        act, h, p = R.choice(S)
        return mcq("%s的时候，钟面是这样。最可能是什么时候？%s" % (act, clock_svg(h, 0)), "%s %d 时" % (p, h),
                   ["%s %d 时" % ("晚上" if p != "晚上" else "上午", h), "%s %d 时" % (p, h % 12 + 1), "%s %d 时" % (p, 12 if h != 12 else 6)],
                   "钟面是 %d 时。%s一般在<b>%s %d 时</b>。" % (h, act, p, h))
    return mk


# ------------------------------------------------------------------ 人民币
COIN = {"1角": (16, "#d9dde0", "#6c7378"), "5角": (18, "#e9c46a", "#a57c00"), "1元": (21, "#d9dde0", "#6c7378")}
NOTE = {"1元": "#b7d7a8", "5元": "#c9a0dc", "10元": "#8fb3e0", "20元": "#d2b48c", "50元": "#9fd3c7", "100元": "#f4a6a6"}
VAL = {"1角": 1, "5角": 5, "1元": 10, "5元": 50, "10元": 100, "20元": 200, "50元": 500, "100元": 1000}   # 角


def money_svg(items):
    s, x, H = [], 8, 66
    for it in items:
        if it[1] == "c":
            r, f, st = COIN[it[0]]
            s.append("<circle cx='%.1f' cy='33' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x + r, r, f, st))
            s.append(text(x + r, 38, it[0], 11 if len(it[0]) > 1 else 12))
            x += 2 * r + 8
        else:
            s.append("<rect x='%d' y='8' width='88' height='50' rx='4' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, NOTE[it[0]], INK))
            s.append(text(x + 44, 39, it[0], 16))
            x += 96
    return fig(svg_wrap(x, H, "".join(s), "人民币"))


def yuan(j):
    """角 → 「3元5角」"""
    y, a = divmod(j, 10)
    if y and a:
        return "%d元%d角" % (y, a)
    return "%d元" % y if y else "%d角" % a


def m_name():
    def mk():
        k = R.choice(list(COIN) + list(NOTE))
        it = (k, "c" if k in COIN and (k != "1元" or R.random() < 0.5) else "n")
        return mcq("这是多少钱？%s" % money_svg([it]), k, R.sample([x for x in ["1角", "5角", "1元", "5元", "10元", "20元", "50元", "100元"] if x != k], 3),
                   "上面写着“%s”，是 <b>%s</b>。" % (k, k))
    return mk


def m_change():
    S = [("1元", "角", 10), ("1角", "分", 10), ("5元", "1元", 5), ("10元", "5元", 2), ("10元", "1元", 10), ("20元", "10元", 2), ("50元", "10元", 5),
         ("100元", "50元", 2), ("100元", "10元", 10), ("1元", "5角", 2), ("5角", "1角", 5), ("20元", "5元", 4), ("50元", "5元", 10)]
    pool = S[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        a, b, n = pool.pop()
        if b in ("角", "分"):
            return mcq("1%s ＝ ？%s" % (a[1:] if a.startswith("1") else a, b), "%d%s" % (n, b), ["%d%s" % (x, b) for x in (100, 1, 5, 20) if x != n],
                       "<b>1%s ＝ %d%s</b>。" % (a[1:], n, b))
        return mcq("一张%s可以换几张（个）%s？" % (a, b), "%d 张" % n if b not in COIN else "%d 个" % n,
                   [("%d 张" if b not in COIN else "%d 个") % x for x in (n + 1, n - 1, n * 2, n + 5) if x > 0],
                   "%s是 %d 个 %s，可以换 <b>%d</b> %s。" % (a, n, b, n, "张" if b not in COIN else "个"))
    return mk


def m_sum(max_j):
    def mk():
        k = R.randint(2, 4)
        pool = [x for x in VAL if VAL[x] <= max_j]
        items = sorted(R.sample(pool, min(k, len(pool))), key=lambda x: -VAL[x])
        extra = R.choice(items)
        items = sorted(items + [extra], key=lambda x: -VAL[x])
        tot = sum(VAL[x] for x in items)
        if tot > max_j:
            return None
        pic = money_svg([(x, "c" if x in COIN and x != "1元" else ("c" if x == "1元" and R.random() < 0.5 else "n")) for x in items])
        w = [yuan(tot + d) for d in (10, -10, 5, -5, 1) if tot + d > 0]
        if tot % 10 and tot > 10:
            w.insert(0, "%d元%d角" % (tot % 10, tot // 10))
        return mcq("一共是多少钱？%s" % pic, yuan(tot), w, "从大面值开始数：%s，一共 <b>%s</b>。" % (" ＋ ".join(items), yuan(tot)))
    return mk


def m_cmp():
    def mk():
        a, b = R.sample(range(3, 120), 2)
        if a // 10 == 0 or b // 10 == 0:
            return None
        ok = ">" if a > b else "<"
        return mcq("%s ○ %s，○ 里填什么？" % (yuan(a), yuan(b)), ok, [x for x in (">", "<", "=", "＋") if x != ok],
                   "%s ＝ %d角，%s ＝ %d角，所以填 <b>%s</b>。" % (yuan(a), a, yuan(b), b, ok))
    return mk


THINGS = [("铅笔", 5, 15), ("橡皮", 3, 12), ("练习本", 10, 30), ("尺子", 8, 20), ("面包", 25, 60), ("牛奶", 30, 50), ("苹果", 15, 40),
          ("气球", 10, 25), ("小汽车玩具", 120, 300), ("故事书", 150, 400), ("文具盒", 120, 260), ("跳绳", 50, 90), ("毛巾", 60, 120), ("雨伞", 200, 400)]


def m_buy(max_j):
    def mk():
        t, lo, hi = R.choice(THINGS)
        if hi > max_j:
            return None
        p = R.randrange(lo, hi + 1)
        if R.random() < 0.5 and p > 10:
            notes = [x for x in (10, 50, 100, 200, 500, 1000) if x >= p and x <= max_j * 2]
            if not notes:
                return None
            pay = notes[0]
            ch = pay - p
            return mcq("%s %s。付了 %s，应找回多少钱？" % (t, yuan(p), yuan(pay)), yuan(ch),
                       [yuan(ch + d) for d in (10, -10, 1, -1) if ch + d > 0] + [yuan(pay + p)],
                       "%s － %s ＝ <b>%s</b>。" % (yuan(pay), yuan(p), yuan(ch)))
        t2, lo2, hi2 = R.choice([x for x in THINGS if x[0] != t and x[2] <= max_j])
        q2 = R.randrange(lo2, hi2 + 1)
        if p + q2 > max_j:
            return None
        return mcq("买一个%s %s，买一个%s %s，一共要多少钱？" % (t, yuan(p), t2, yuan(q2)), yuan(p + q2),
                   [yuan(p + q2 + d) for d in (10, -10, 1, -1) if p + q2 + d > 0] + [yuan(abs(p - q2)) if p != q2 else None],
                   "%s ＋ %s ＝ <b>%s</b>。（元和元加，角和角加，满 10 角换 1 元）" % (yuan(p), yuan(q2), yuan(p + q2)))
    return mk


# ------------------------------------------------------------------ 找规律
COLN = {"red": "红色", "blue": "蓝色", "yellow": "黄色", "green": "绿色"}
SHN = {"circle": "圆", "triangle": "三角形", "square": "正方形"}
PATS = ["AB", "AAB", "ABB", "ABC", "AABB"]


def pat(kind):
    def mk():
        p = R.choice(PATS)
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        if kind == "obj":
            ks = R.sample(KINDS, len(set(p)))
            mp = {ch: ks[i] for i, ch in enumerate(sorted(set(p)))}
            seq = [mp[p[i % len(p)]] for i in range(L + 1)]
            pic = zh(pattern_svg([("obj", k) for k in seq[:-1]], 1), "按规律排的东西")
            return mcq("按规律接着排，? 处应该是什么？%s" % pic, nm(seq[-1]), [nm(k) for k in ks if k != seq[-1]] + [nm(k) for k in KINDS if k not in ks][:2],
                       "%s一组，重复出现。? 处是<b>%s</b>。" % ("、".join(nm(mp[c]) for c in p), nm(seq[-1])))
        if kind == "color":
            cs = R.sample(list(COLN), len(set(p)))
            mp = {ch: cs[i] for i, ch in enumerate(sorted(set(p)))}
            shp = R.choice(list(SHN))
            seq = [mp[p[i % len(p)]] for i in range(L + 1)]
            pic = zh(pattern_svg([("shape", shp, c) for c in seq[:-1]], 1), "按规律涂色")
            return mcq("按规律涂色，? 处应该涂什么颜色？%s" % pic, COLN[seq[-1]], [COLN[c] for c in COLN if c != seq[-1]],
                       "%s一组，重复出现。? 处涂<b>%s</b>。" % ("、".join(COLN[mp[c]] for c in p), COLN[seq[-1]]))
        ss = R.sample(list(SHN), len(set(p)))
        mp = {ch: ss[i] for i, ch in enumerate(sorted(set(p)))}
        col = R.choice(list(COLN))
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        pic = zh(pattern_svg([("shape", s, col) for s in seq[:-1]], 1), "按规律排的图形")
        return mcq("按规律接着排，? 处应该是什么图形？%s" % pic, SHN[seq[-1]], [SHN[s] for s in SHN if s != seq[-1]] + ["长方形"],
                   "%s一组，重复出现。? 处是<b>%s</b>。" % ("、".join(SHN[mp[c]] for c in p), SHN[seq[-1]]))
    return mk


def pat_num():
    def mk():
        if R.random() < 0.5:
            st = R.choice([1, 2, 5, 10])
            down = R.random() < 0.3
            a = R.randint(1, 100 - st * 6)
            sq = [a + st * i for i in range(6)]
            if down:
                sq = sq[::-1]
            ans = sq[-1]
            return mcq("按规律填数：%s，（　）" % "，".join(str(x) for x in sq[:-1]), str(ans),
                       [str(x) for x in (ans + 1, ans - 1, ans + st, ans - st, ans + 10) if x > 0 and x != ans],
                       "每次%s %d，所以填 <b>%d</b>。" % ("减少" if down else "增加", st, ans))
        p = R.choice(["AB", "ABC", "AAB", "ABB"])
        ns = R.sample(range(1, 10), len(set(p)))
        mp = {ch: ns[i] for i, ch in enumerate(sorted(set(p)))}
        L = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(L + 1)]
        return mcq("按规律填数：%s，（　）" % "，".join(str(x) for x in seq[:-1]), str(seq[-1]), [str(x) for x in ns if x != seq[-1]] + [str(seq[-1] + 1)],
                   "%s一组重复出现，所以填 <b>%d</b>。" % ("、".join(str(mp[c]) for c in p), seq[-1]))
    return mk


def pat_mid():
    def mk():
        p = R.choice(PATS)
        ks = R.sample(KINDS, len(set(p)))
        mp = {ch: ks[i] for i, ch in enumerate(sorted(set(p)))}
        L = len(p) * 3
        seq = [mp[p[i % len(p)]] for i in range(L)]
        b = R.randint(len(p), L - 2)
        items = [("obj", k) if i != b else ("blank",) for i, k in enumerate(seq)]
        return mcq("按规律排，中间的 ? 应该是什么？%s" % zh(pattern_svg(items, 0), "按规律排的东西"), nm(seq[b]),
                   [nm(k) for k in ks if k != seq[b]] + [nm(k) for k in KINDS if k not in ks][:2],
                   "%s一组重复，? 处是<b>%s</b>。" % ("、".join(nm(mp[c]) for c in p), nm(seq[b])))
    return mk


def clocks_abcd(times, size=110):
    """4 個の小さな钟面に A〜D"""
    parts = []
    for i, (h, m) in enumerate(times):
        c = clock_svg(h, m, size)
        inner = c.split(">", 2)[2].rsplit("</svg>", 1)[0] if c.startswith("<div") else ""
        parts.append((i, inner))
    import re
    s = []
    for i, (h, m) in enumerate(times):
        svg = clock_svg(h, m, size)
        body = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
        s.append("<g transform='translate(%d 24)'>%s</g>" % (i * (size + 14), body))
        s.append(text(i * (size + 14) + size / 2, 18, LET[i], 16, col=GREEN))
    return fig(svg_wrap(4 * (size + 14), size + 30, "".join(s), "4 个钟面"))


def t_which(half=False):
    def mk():
        h = R.randint(1, 12)
        m = 30 if half else 0
        cands = [(h, m), (h % 12 + 1, m), ((h + 5) % 12 + 1, 0 if half else 30), (h, 30 if m == 0 else 0)]
        if not half:
            cands[3] = (12 if h != 12 else 6, h % 12 if h % 12 else 0)
            cands[3] = ((h + 5) % 12 + 1, 0) if cands[3][1] not in (0, 30) else cands[3]
        if len(set(cands)) < 4:
            return None
        order = list(range(4))
        R.shuffle(order)
        times = [cands[i] for i in order]
        a = LET[order.index(0)]
        return mcq("哪一个钟面是 %d 时%s？%s" % (h, " 30 分" if half else "", clocks_abcd(times)), a, [x for x in LET if x != a],
                   "%s时针%s %d，分针指着 %s。是 <b>%s</b>。" % ("", "刚过" if half else "指着", h, "6" if half else "12", a))
    return mk


def t_after():
    def mk():
        h = R.randint(1, 11)
        k = R.choice([1, 2, 3])
        half = R.random() < 0.3
        if half:
            return mcq("现在是 %d 时，再过半小时是几时几分？%s" % (h, clock_svg(h, 0)), "%d 时 30 分" % h,
                       ["%d 时 30 分" % (h + 1), "%d 时" % (h + 1), "%d 时 30 分" % (h - 1 if h > 1 else 12)],
                       "半小时后分针走到 6，时针还没到 %d，是 <b>%d 时 30 分</b>。" % (h + 1, h))
        a = (h + k - 1) % 12 + 1
        return mcq("现在是 %d 时，再过 %d 小时是几时？%s" % (h, k, clock_svg(h, 0)), "%d 时" % a,
                   ["%d 时" % x for x in ((a % 12) + 1, (h - k - 1) % 12 + 1, h, k) if x != a],
                   "时针从 %d 往前走 %d 个大格，是 <b>%d 时</b>。" % (h, k, a))
    return mk
