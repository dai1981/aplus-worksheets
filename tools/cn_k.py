# -*- coding: utf-8 -*-
"""
中国 幼儿园大班（5～6岁）数学。《3-6岁儿童学习与发展指南》科学领域・数学认知（目标1〜3）。
10 以内（数えるのは 20 まで）、とても短い文、ほぼ全問に絵。cn_low の問題と、ここで作る問題を使う。
python3 tools/cn_k.py [slug…]
"""
import random
import k_pics as K
import cn_low as L
from f_common import pictograph_svg, pattern_svg
from ws_common import svg_wrap, text, INK, GREEN
from cn_common import unit, build_sets, lesson, mcq, GIRLS

G = 0
LET = "ABCD"
R = random.Random(0)


def setup(rnd):
    global R
    R = rnd
    L.setup(rnd)


def nm(k):
    return L.nm(k)


def cl(k):
    return L.cl(k)


zh = L.zh


def name():
    return L.NM.next()


def ta(n):
    return "她" if n in GIRLS else "他"


def abcd(ans_i):
    return LET[ans_i], [x for i, x in enumerate(LET) if i != ans_i]


# ------------------------------------------------------------------ 数
WORD = "零一二三四五六七八九十"


def num_word():
    pool = [(n, d) for n in range(0, 11) for d in (0, 1)]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        n, d = pool.pop()
        if d == 0:
            w = [str(x) for x in L.near(n, 0, 10)]
            return mcq("汉字“%s”是数字几？" % WORD[n], str(n), w, "“%s”就是 <b>%d</b>。" % (WORD[n], n))
        w = [WORD[x] for x in L.near(n, 0, 10)]
        return mcq("数字 %d 用汉字怎么写？" % n, WORD[n], w, "%d 写作“<b>%s</b>”。" % (n, WORD[n]))
    return mk


def which_group(lo, hi):
    """哪一组正好有 n 个"""
    def mk():
        k = R.choice(L.KINDS)
        n = R.randint(lo, hi)
        others = [x for x in range(max(1, n - 3), min(10, n + 3) + 1) if x != n]
        if len(others) < 3:
            return None
        cnt = R.sample(others, 3) + [n]
        R.shuffle(cnt)
        a = cnt.index(n)
        pic = zh(K.lettered_groups_svg([(c, k) for c in cnt]), "四组%s" % nm(k))
        return mcq("哪一组正好有 %d%s%s？%s" % (n, cl(k), nm(k), pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                   "一个一个地数，%s 组有 <b>%d%s</b>。" % (LET[a], n, cl(k)))
    return mk


def most_group():
    """哪一组最多 / 最少"""
    def mk():
        k = R.choice(L.KINDS)
        cnt = R.sample(range(1, 11), 4)
        most = R.random() < 0.5
        t = max(cnt) if most else min(cnt)
        a = cnt.index(t)
        pic = zh(K.lettered_groups_svg([(c, k) for c in cnt]), "四组%s" % nm(k))
        return mcq("哪一组的%s最%s？%s" % (nm(k), "多" if most else "少", pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                   "数一数：%s。%s 组有 %d%s，最%s。答案是 <b>%s</b>。" % ("、".join("%s 组 %d" % (LET[i], c) for i, c in enumerate(cnt)),
                                                                   LET[a], t, cl(k), "多" if most else "少", LET[a]))
    return mk


def biggest(lo, hi):
    def mk():
        ns = R.sample(range(lo, hi + 1), 4)
        big = R.random() < 0.5
        t = max(ns) if big else min(ns)
        return mcq("%s，哪个数最%s？" % ("、".join(map(str, ns)), "大" if big else "小"), str(t), [str(x) for x in ns],
                   "按顺序数，%s 排在最%s面，所以 <b>%d</b> 最%s。" % (t, "后" if big else "前", t, "大" if big else "小"))
    return mk


def tf20():
    TF = ["dot", "apple", "star", "flower", "ball"]

    def mk():
        n, k = R.randint(11, 20), R.choice(TF)
        u = "朵" if k == "flower" else "个"
        return mcq("两个十格图里一共有几%s？%s" % (u, zh(K.tenframe_svg(n, 2, k), "两个十格图")), "%d%s" % (n, u),
                   ["%d%s" % (x, u) for x in L.near(n, 10, 20) + [n - 10]],
                   "第一个十格图是满的，是 10；第二个有 %d%s。10 和 %d 合起来是 <b>%d%s</b>。" % (n - 10, u, n - 10, n, u))
    return mk


def ten_and():
    pool = [(o, how) for o in range(1, 11) for how in (0, 1)]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        o, how = pool.pop()
        n = 10 + o
        if how == 0:
            return mcq("10 和 %d 合起来是几？" % o, str(n), [str(x) for x in (o, n + 1, n - 1, 100 + o if o < 10 else 30)],
                       "10 后面再数 %d 个：%s。是 <b>%d</b>。" % (o, "、".join(str(10 + i) for i in range(1, o + 1)), n))
        return mcq("%d 是 10 和几合起来的？" % n, str(o), [str(x) for x in (n, o + 1, o - 1 if o > 1 else 12, 10)],
                   "10 和 %d 合起来是 %d，所以填 <b>%d</b>。" % (o, n, o))
    return mk


# ------------------------------------------------------------------ 按群计数
def group_count(size):
    def mk():
        k = R.choice(L.KINDS)
        g = R.randint(2, 20 // size)
        if size * g < 4:
            return None
        n = size * g
        pic = zh(K.groups_svg([(size, k)] * g, 26), "%d组%s，每组%d%s" % (g, nm(k), size, cl(k)))
        return mcq("%d%s%d%s地数，一共有几%s？%s" % (size, cl(k), size, cl(k), cl(k), pic), "%d%s" % (n, cl(k)),
                   ["%d%s" % (x, cl(k)) for x in (n + size, n - size, n + 1, n - 1, g) if 0 < x <= 25 and x != n],
                   "%s，一共 <b>%d%s</b>。" % ("、".join(str(size * i) for i in range(1, g + 1)), n, cl(k)))
    return mk


def plates():
    def mk():
        k = R.choice(L.KINDS)
        size = R.choice([2, 2, 3, 4, 5])
        g = R.randint(2, min(5, 20 // size))
        n = size * g
        pics = "".join(zh(K.plate_svg(size, k, 5), "盘子") for _ in range(g))
        return mcq("每个盘子里有 %d%s%s，%d 个盘子一共有几%s？%s" % (size, cl(k), nm(k), g, cl(k), pics), "%d%s" % (n, cl(k)),
                   ["%d%s" % (x, cl(k)) for x in (n + size, n - size, size + g, n + 1) if 0 < x and x != n],
                   "%d 个 %d 个地数：%s，一共 <b>%d%s</b>。" % (size, size, "、".join(str(size * i) for i in range(1, g + 1)), n, cl(k)))
    return mk


def skip_seq(steps=(2, 5)):
    def mk():
        st = R.choice(steps)
        Ln = 5
        top = 20 if st < 5 else 30
        a = R.randrange(0, top - st * (Ln - 1) + 1)
        sq = [a + st * i for i in range(Ln)]
        p = R.randint(1, Ln - 1)
        ans = sq[p]
        shown = ["?" if i == p else str(x) for i, x in enumerate(sq)]
        return mcq("%d 个 %d 个地数，? 是几？%s" % (st, st, zh(K.cards_svg(shown), "数字卡片")), str(ans),
                   [str(x) for x in (ans + 1, ans - 1, ans + st, ans - st) if x >= 0 and x != ans],
                   "每次多 %d：%s 后面是 <b>%d</b>。" % (st, sq[p - 1], ans))
    return mk


def pairs():
    S = [("袜子", "双", "只", 2), ("鞋", "双", "只", 2), ("手套", "双", "只", 2), ("筷子", "双", "根", 2)]

    def mk():
        t, u, v, s = R.choice(S)
        g = R.randint(2, 9)
        if R.random() < 0.5:
            return mcq("一%s%s是 2 %s。%d %s%s一共有几%s？" % (u, t, v, g, u, t, v), "%d %s" % (g * 2, v),
                       ["%d %s" % (x, v) for x in (g, g + 2, g * 2 + 2, g * 2 - 2)],
                       "2 个 2 个地数：%s，一共 <b>%d %s</b>。" % ("、".join(str(2 * i) for i in range(1, g + 1)), 2 * g, v))
        return mcq("%d %s%s，能配成几%s？" % (2 * g, v, t, u), "%d %s" % (g, u),
                   ["%d %s" % (x, u) for x in (2 * g, g + 1, g - 1, g + 2)],
                   "2 %s配 1 %s：%s，一共 <b>%d %s</b>。" % (v, u, "、".join(str(2 * i) for i in range(1, g + 1)), g, u))
    return mk


# ------------------------------------------------------------------ 比多少
def more_by():
    def mk():
        ka, kb = R.sample(L.KINDS, 2)
        a, b = R.sample(range(1, 11), 2)
        pic = zh(K.match_svg([(a, ka, "", None), (b, kb, "", None)]), "上下两行东西")
        big, small = (ka, kb) if a > b else (kb, ka)
        d = abs(a - b)
        if R.random() < 0.5:
            q = "%s比%s多几个？%s" % (nm(big), nm(small), pic)
            e = "一个对一个，%s多出 <b>%d 个</b>。" % (nm(big), d)
        else:
            q = "%s比%s少几个？%s" % (nm(small), nm(big), pic)
            e = "一个对一个，%s少了 <b>%d 个</b>。" % (nm(small), d)
        return mcq(q, "%d 个" % d, ["%d 个" % x for x in (d + 1, d - 1, max(a, b), min(a, b)) if x > 0 and x != d], e)
    return mk


def cmp_trap():
    """大的不一定多：间隔宽的不一定多"""
    def mk():
        ka, kb = R.sample(L.KINDS, 2)
        a = R.randint(3, 9)
        b = R.choice([x for x in (a - 2, a - 1, a, a + 1) if 2 <= x <= 10])
        pic = zh(K.match_svg([(a, ka, "", 32), (b, kb, "", 56)]), "上下两行东西")
        ok = "%s多" % nm(ka) if a > b else "%s多" % nm(kb) if b > a else "一样多"
        e = "下面一行排得宽，看起来长，但要数一数：%s %d%s，%s %d%s。答案：<b>%s</b>。" % (nm(ka), a, cl(ka), nm(kb), b, cl(kb), ok)
        return mcq("%s和%s，哪种多？%s" % (nm(ka), nm(kb), pic), ok, ["%s多" % nm(ka), "%s多" % nm(kb), "一样多", "排得长的多"], e)
    return mk


SNACK = [("糖", "颗"), ("饼干", "块"), ("贴纸", "张"), ("气球", "个"), ("小红花", "朵"), ("玻璃珠", "颗"), ("草莓", "个"), ("积木", "块")]


def cmp_story():
    def mk():
        a, b = name(), name()
        if a == b:
            return None
        t, u = R.choice(SNACK)
        x, y = R.sample(range(1, 11), 2)
        how = R.random()
        if how < 0.4:
            w = a if x > y else b
            return mcq("%s有 %d %s%s，%s有 %d %s%s。谁的%s多？" % (a, x, u, t, b, y, u, t, t), w, [b if w == a else a, "一样多", "不能比"],
                       "%d 比 %d 大，所以 <b>%s</b>的%s多。" % (max(x, y), min(x, y), w, t))
        d = abs(x - y)
        big, small = (a, b) if x > y else (b, a)
        return mcq("%s有 %d %s%s，%s有 %d %s%s。%s比%s多几%s？" % (a, x, u, t, b, y, u, t, big, small, u), "%d %s" % (d, u),
                   ["%d %s" % (v, u) for v in (d + 1, d - 1, x + y, max(x, y)) if v > 0 and v != d],
                   "一个对一个比，多出来的是 %d － %d ＝ <b>%d %s</b>。" % (max(x, y), min(x, y), d, u))
    return mk


# ------------------------------------------------------------------ 序数
def queue_ord():
    def mk():
        p = name()
        how = R.random()
        if how < 0.35:
            f = R.randint(1, 8)
            return mcq("小朋友排队。%s前面有 %d 人，%s排第几？" % (p, f, ta(p)), "第 %d" % (f + 1), ["第 %d" % x for x in (f, f + 2, f - 1) if x > 0] + ["第 %d" % (f + 3)],
                       "前面有 %d 人，%s自己是下一个：<b>第 %d</b>。" % (f, ta(p), f + 1))
        if how < 0.7:
            k = R.randint(2, 9)
            return mcq("%s排第 %d。%s前面有几人？" % (p, k, ta(p)), "%d 人" % (k - 1), ["%d 人" % x for x in (k, k + 1, k - 2) if x >= 0] + ["%d 人" % (k + 2)],
                       "第 %d 就是前面有 %d 人，再加%s自己。所以前面有 <b>%d 人</b>。" % (k, k - 1, ta(p), k - 1))
        k = R.randint(2, 6)
        b = R.randint(1, 4)
        n = k + b
        return mcq("%s从前往后数排第 %d，%s后面还有 %d 人。这一队一共有几人？" % (p, k, ta(p), b), "%d 人" % n,
                   ["%d 人" % x for x in (n - 1, n + 1, k, b + 1)], "前面到%s是 %d 人，后面 %d 人：%d ＋ %d ＝ <b>%d 人</b>。" % (ta(p), k, b, k, b, n))
    return mk


def race():
    ANI = ["小猫", "小狗", "小兔", "小熊", "小猴", "小鹿", "小羊", "小猪"]

    def mk():
        ks = R.sample(ANI, 5)
        a = R.choice(ks)
        i = ks.index(a)
        how = R.random() < 0.5
        line = "→".join(ks)
        if how:
            return mcq("赛跑的名次：%s（第一名在最前面）。%s是第几名？" % (line, a), "第%s名" % WORD[i + 1],
                       ["第%s名" % WORD[x + 1] for x in range(5) if x != i], "从第一名数起，%s是 <b>第%s名</b>。" % (a, WORD[i + 1]))
        return mcq("赛跑的名次：%s（第一名在最前面）。第%s名是谁？" % (line, WORD[i + 1]), a, [x for x in ks if x != a],
                   "从前面数到第%s个，是 <b>%s</b>。" % (WORD[i + 1], a))
    return mk


# ------------------------------------------------------------------ 分与合
def hidden():
    def mk():
        k = R.choice(L.KINDS)
        n = R.randint(3, 10)
        v = R.randint(1, n - 1)
        pic = zh(K.box_svg(v, k), "外面的%s和一个盒子" % nm(k))
        return mcq("一共有 %d%s%s，有的藏在盒子里。盒子里有几%s？%s" % (n, cl(k), nm(k), cl(k), pic), "%d%s" % (n - v, cl(k)),
                   ["%d%s" % (x, cl(k)) for x in (v, n, n - v + 1, n - v - 1) if x > 0 and x != n - v],
                   "外面有 %d%s，%d 可以分成 %d 和 %d。盒子里有 <b>%d%s</b>。" % (v, cl(k), n, v, n - v, n - v, cl(k)))
    return mk


def make10():
    TF = ["dot", "apple", "star", "flower", "ball"]

    def mk():
        n, k = R.randint(1, 9), R.choice(TF)
        u = "朵" if k == "flower" else "个"
        return mcq("十格图里有 %d%s。还要放几%s才满 10 格？%s" % (n, u, u, zh(K.tenframe_svg(n, 1, k), "十格图")), "%d%s" % (10 - n, u),
                   ["%d%s" % (x, u) for x in (n, 11 - n, 9 - n, 10) if 0 < x and x != 10 - n],
                   "数空格：%d 和 %d 合成 10，还要 <b>%d%s</b>。" % (n, 10 - n, 10 - n, u))
    return mk


def hands():
    def mk():
        n = R.randint(3, 10)
        a = R.randint(1, n - 1)
        t, u = R.choice(SNACK)
        p = name()
        return mcq("%s有 %d %s%s，左手拿 %d %s，右手拿几%s？" % (p, n, u, t, a, u, u), "%d %s" % (n - a, u),
                   ["%d %s" % (x, u) for x in (a, n, n - a + 1, n - a - 1) if x > 0 and x != n - a],
                   "%d 可以分成 %d 和 %d，右手拿 <b>%d %s</b>。" % (n, a, n - a, n - a, u))
    return mk


# ------------------------------------------------------------------ 加和减
def add_pic():
    def mk():
        k = R.choice(L.KINDS)
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a + b > 10:
            return None
        pic = zh(K.two_groups_svg(a, k, b, k, "和"), "%d%s和%d%s" % (a, cl(k), b, cl(k)))
        return mcq("合起来一共有几%s%s？%s" % (cl(k), nm(k), pic), "%d%s" % (a + b, cl(k)),
                   ["%d%s" % (x, cl(k)) for x in L.near(a + b, 1, 12) + [abs(a - b)]],
                   "%d 和 %d 合起来，%d ＋ %d ＝ <b>%d</b>。" % (a, b, a, b, a + b))
    return mk


def take_pic():
    def mk():
        k = R.choice(L.KINDS)
        n = R.randint(2, 10)
        t = R.randint(1, n - 1)
        pic = zh(K.crossed_row_svg(n, k, t), "%d%s%s，划掉%d%s" % (n, cl(k), nm(k), t, cl(k)))
        return mcq("划掉的是拿走的。还剩几%s？%s" % (cl(k), pic), "%d%s" % (n - t, cl(k)),
                   ["%d%s" % (x, cl(k)) for x in (t, n, n - t + 1, n - t - 1) if x > 0 and x != n - t],
                   "原来有 %d%s，拿走 %d%s，%d － %d ＝ <b>%d</b>。" % (n, cl(k), t, cl(k), n, t, n - t))
    return mk


def calc_pic():
    def mk():
        k = R.choice(L.KINDS)
        if R.random() < 0.5:
            a, b = R.randint(1, 8), R.randint(1, 8)
            if a + b > 10 or a == b:
                return None
            pic = zh(K.two_groups_svg(a, k, b, k, "和"), "两组%s" % nm(k))
            ok = "%d ＋ %d ＝ %d" % (a, b, a + b)
            w = ["%d － %d ＝ %d" % (max(a, b), min(a, b), abs(a - b)), "%d ＋ %d ＝ %d" % (a, b, a + b + 1), "%d ＋ %d ＝ %d" % (a, a, 2 * a)]
            return mcq("哪个算式和图对得上（合起来）？%s" % pic, ok, w, "两部分合起来用加法：<b>%s</b>。" % ok)
        n = R.randint(3, 10)
        t = R.randint(1, n - 1)
        pic = zh(K.crossed_row_svg(n, k, t), "划掉了一些%s" % nm(k))
        ok = "%d － %d ＝ %d" % (n, t, n - t)
        w = ["%d ＋ %d ＝ %d" % (n, t, n + t), "%d － %d ＝ %d" % (n, n - t, t) if n - t != t else "%d － %d ＝ %d" % (n, t, n - t + 1),
             "%d － %d ＝ %d" % (n, t, n - t - 1) if n - t > 1 else "%d ＋ %d ＝ %d" % (t, n, n + t)]
        return mcq("划掉的是拿走的。哪个算式对？%s" % pic, ok, w, "从 %d 里去掉 %d，用减法：<b>%s</b>。" % (n, t, ok))
    return mk


ADD = [("树上有 %d 只小鸟，又飞来 %d 只。现在有几只？", "只"), ("池塘里有 %d 只鸭子，又游来 %d 只。现在有几只？", "只"),
       ("%s有 %d 颗糖，妈妈又给了 %d 颗。现在有几颗？", "颗"), ("盘子里有 %d 个饺子，又放进 %d 个。盘子里有几个？", "个"),
       ("花园里开了 %d 朵红花和 %d 朵黄花。一共有几朵？", "朵"), ("%s搭了 %d 块积木，又搭了 %d 块。一共几块？", "块"),
       ("车上有 %d 人，又上来 %d 人。车上有几人？", "人"), ("左边有 %d 只小兔，右边有 %d 只小兔。一共有几只？", "只")]
SUB = [("树上有 %d 只小鸟，飞走了 %d 只。还剩几只？", "只"), ("%s有 %d 块饼干，吃了 %d 块。还剩几块？", "块"),
       ("盘子里有 %d 个苹果，拿走了 %d 个。还剩几个？", "个"), ("有 %d 个气球，飞走了 %d 个。还剩几个？", "个"),
       ("车上有 %d 人，下去了 %d 人。还剩几人？", "人"), ("%s有 %d 张贴纸，送给朋友 %d 张。还剩几张？", "张"),
       ("河里有 %d 条小鱼，游走了 %d 条。还剩几条？", "条"), ("篮子里有 %d 个鸡蛋，用了 %d 个。还剩几个？", "个")]


def story(kind):
    def mk():
        tpl, u = R.choice(ADD if kind == "add" else SUB)
        if kind == "add":
            a, b = R.randint(1, 9), R.randint(1, 9)
            if a + b > 10:
                return None
            ans, e = a + b, "合起来用加法：%d ＋ %d ＝ <b>%d %s</b>。" % (a, b, a + b, u)
            w = [a + b + 1, a + b - 1, abs(a - b), max(a, b)]
        else:
            a = R.randint(2, 10)
            b = R.randint(1, a - 1)
            ans, e = a - b, "去掉用减法：%d － %d ＝ <b>%d %s</b>。" % (a, b, a - b, u)
            w = [a - b + 1, a - b - 1, a + b, b]
        q = tpl % ((name(), a, b) if tpl.startswith("%s") else (a, b))
        return mcq(q, "%d %s" % (ans, u), ["%d %s" % (x, u) for x in w if 0 <= x and x != ans], e)
    return mk


# ------------------------------------------------------------------ 比较：长短、高矮、粗细、厚薄、轻重
def longest():
    def mk():
        ls = R.sample(range(3, 10), 4)
        lg = R.random() < 0.5
        t = max(ls) if lg else min(ls)
        a = ls.index(t)
        pic = zh(K.pencils_svg(ls), "四支铅笔")
        return mcq("哪一支铅笔最%s？%s" % ("长" if lg else "短", pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                   "左边对齐，看右边哪支伸得最%s：<b>%s</b>。" % ("远" if lg else "近", LET[a]))
    return mk


def offset_len():
    """左端がそろっていない：本当の長さで比べる"""
    def mk():
        a, b = R.sample(range(3, 8), 2)
        oa, ob = (0, R.randint(2, 3)) if a > b else (R.randint(2, 3), 0)
        pic = zh(K.pencils_svg([a, b], ["A", "B"], offsets=[oa, ob]), "两支铅笔")
        ok = "A" if a > b else "B"
        return mcq("A 和 B 哪一支铅笔长？（看清两头）%s" % pic, ok, ["B" if ok == "A" else "A", "一样长", "不能比"],
                   "两支铅笔的左边没有对齐。看两头之间有多长：<b>%s</b> 长。" % ok)
    return mk


def tallest():
    def mk():
        hs = R.sample(range(2, 9), 4)
        hi = R.random() < 0.5
        t = max(hs) if hi else min(hs)
        a = hs.index(t)
        pic = zh(K.towers_svg(hs), "四座积木塔")
        return mcq("哪一座积木塔最%s？%s" % ("高" if hi else "矮", pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                   "底下对齐，看谁最%s：<b>%s</b>。" % ("高" if hi else "矮", LET[a]))
    return mk


def tower_more():
    def mk():
        hs = R.sample(range(2, 9), 2)
        pic = zh(K.towers_svg(hs, ["A", "B"]), "两座积木塔")
        d = abs(hs[0] - hs[1])
        hi = "A" if hs[0] > hs[1] else "B"
        lo = "B" if hi == "A" else "A"
        return mcq("%s 塔比 %s 塔高几块积木？%s" % (hi, lo, pic), "%d 块" % d, ["%d 块" % x for x in (d + 1, d - 1, max(hs), min(hs)) if x > 0 and x != d],
                   "%s 塔 %d 块，%s 塔 %d 块，高 <b>%d 块</b>。" % (hi, max(hs), lo, min(hs), d))
    return mk


COLS = ["#c8935a", "#7fb3e6", "#e59866", "#82c785"]


def sticks_svg(ws, what):
    """粗细（立てた棒・木）か 厚薄（横に寝かせた本）"""
    s = []
    if what == "thick":
        H, sp = 120, 70
        for i, w in enumerate(ws):
            cx = 10 + sp / 2 + i * sp
            s.append("<rect x='%.1f' y='10' width='%d' height='%d' rx='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx - w / 2, w, H, min(4, w // 3), COLS[i], INK))
            s.append(text(cx, H + 34, LET[i], 18, col=GREEN))
        return svg_wrap(20 + sp * len(ws), H + 42, "".join(s), "粗细不同的棒")
    base, sp = 100, 80
    for i, w in enumerate(ws):
        x = 10 + i * sp
        s.append("<rect x='%d' y='%d' width='64' height='%d' rx='2' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, base - w, w, COLS[i], INK))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#ffffff' stroke-width='1.4'/>" % (x + 6, base - w + 3, x + 6, base - 3))
        s.append(text(x + 32, base + 26, LET[i], 18, col=GREEN))
    s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (base, 10 + sp * len(ws), base, INK))
    return svg_wrap(20 + sp * len(ws), base + 34, "".join(s), "厚薄不同的书")


def thick():
    def mk():
        what = R.choice(["thick", "book"])
        ws = R.sample([6, 10, 14, 18, 24, 30, 36] if what == "thick" else [6, 12, 18, 26, 34, 44, 54], 4)
        big = R.random() < 0.5
        t = max(ws) if big else min(ws)
        a = ws.index(t)
        pic = zh(sticks_svg(ws, what), "四根棒" if what == "thick" else "四本书")
        if what == "thick":
            return mcq("哪一根木棒最%s？%s" % ("粗" if big else "细", pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                       "木棒一样长，看哪根最%s：<b>%s</b>。" % ("宽" if big else "窄", LET[a]))
        return mcq("哪一本书最%s？%s" % ("厚" if big else "薄", pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                   "书平放在桌上，看哪本最%s：<b>%s</b>。" % ("高" if big else "矮", LET[a]))
    return mk


def heavy():
    def mk():
        ka, kb = R.sample(["apple", "ball", "cup"], 2)       # 大きさの近いものだけ
        na, nb = R.randint(1, 3), R.randint(1, 3)
        tilt = R.choice(["left", "right", "equal"])
        pic = zh(K.balance_svg((ka, na), (kb, nb), tilt), "天平")
        if tilt == "equal":
            ok = "一样重"
            e = "天平平平的，两边 <b>一样重</b>。"
        else:
            h = ka if tilt == "left" else kb
            ok = "%s那边重" % nm(h)
            e = "重的一边往下沉。%s那边低，所以 <b>%s</b>。" % (nm(h), ok)
        return mcq("天平左边是%s，右边是%s。哪边重？%s" % (nm(ka), nm(kb), pic), ok, ["%s那边重" % nm(ka), "%s那边重" % nm(kb), "一样重", "看不出来"], e)
    return mk


THINGS2 = [("西瓜", "苹果", "重"), ("大象", "小狗", "重"), ("书包", "铅笔", "重"), ("羽毛", "石头", "轻"), ("气球", "皮球", "轻"),
           ("树叶", "砖头", "轻"), ("电视机", "遥控器", "重"), ("小汽车", "自行车", "重"), ("纸巾", "字典", "轻"), ("鸡蛋", "冬瓜", "轻")]
LEN2 = [("火车", "小汽车", "长"), ("跳绳", "鞋带", "长"), ("长颈鹿的脖子", "小鸭的脖子", "长"), ("筷子", "牙签", "长"), ("毛毛虫", "蛇", "短"),
        ("大楼", "小房子", "高"), ("爸爸", "宝宝", "高"), ("小草", "大树", "矮"), ("凳子", "桌子", "矮")]


def life_cmp():
    pool = []
    for a, b, w in THINGS2 + LEN2:
        pool.append((a, b, w))
    R.shuffle(pool)
    OPP = {"重": "轻", "轻": "重", "长": "短", "短": "长", "高": "矮", "矮": "高"}

    def mk():
        if not pool:
            return None
        a, b, w = pool.pop()
        x, y = (a, b) if R.random() < 0.5 else (b, a)
        return mcq("%s和%s，哪个%s？" % (x, y, w), a, [b, "一样%s" % w, "不能比"], "<b>%s</b>比%s%s。" % (a, b, w))
    return mk


def relative():
    """量的相对性：A 比 B 高，B 比 C 高"""
    W = [("高", "矮"), ("长", "短"), ("重", "轻")]

    def mk():
        big, small = R.choice(W)
        if big == "长":
            ps = R.sample(["红绳", "蓝绳", "黄绳", "绿绳", "白绳"], 3)
        elif big == "重":
            ps = R.sample(["西瓜", "南瓜", "冬瓜", "菠萝", "椰子"], 3)
        else:
            ps = [name() for _ in range(3)]
            if len(set(ps)) < 3:
                return None
        a, b, c = ps                     # a > b > c
        how = R.random()
        if how < 0.35:
            q = "%s比%s%s，%s比%s%s。谁最%s？" % (a, b, big, b, c, big, big)
            return mcq(q, a, [b, c, "一样%s" % big], "%s > %s > %s，最%s的是 <b>%s</b>。" % (a, b, c, big, a))
        if how < 0.7:
            q = "%s比%s%s，%s比%s%s。谁最%s？" % (a, b, big, b, c, big, small)
            return mcq(q, c, [a, b, "一样%s" % small], "%s > %s > %s（按%s排），最%s的是 <b>%s</b>。" % (a, b, c, big, small, c))
        q = "%s比%s%s，%s比%s%s。%s是最%s的吗？" % (a, b, big, b, c, big, b, big)
        return mcq(q, "不是，%s比%s%s，比%s%s" % (b, a, small, c, big), ["是，%s最%s" % (b, big), "是，%s最%s" % (b, small), "不是，%s最%s" % (c, big)],
                   "%s在中间：<b>比%s%s，比%s%s</b>。同一个东西，和不同的比，结果不一样。" % (b, a, small, c, big))
    return mk


# ------------------------------------------------------------------ 图形
SHP = {"circle": "圆形", "triangle": "三角形", "square": "正方形", "rectangle": "长方形", "hexagon": "六边形"}
SHPS = list(SHP)
CLRS = ["red", "blue", "yellow", "green"]
CLRN = {"red": "红色", "blue": "蓝色", "yellow": "黄色", "green": "绿色"}


def shape_name():
    def mk():
        k = R.choice(SHPS)
        rot = R.choice([0, 10, 20]) if k != "circle" else 0
        r = R.choice([34, 40, 46])
        pic = zh(K.one_shape_svg(k, R.choice(CLRS), r, rot), "一个图形")
        tip = {"circle": "圆圆的，没有角，是", "triangle": "有 3 条边、3 个角，是", "square": "有 4 条一样长的边、4 个直角，是",
               "rectangle": "有 4 个直角，对边一样长，长长的，是", "hexagon": "有 6 条边、6 个角，是"}[k]
        return mcq("这是什么图形？%s" % pic, SHP[k], [SHP[x] for x in SHPS if x != k], "%s<b>%s</b>。" % (tip, SHP[k]))
    return mk


def which_shape():
    def mk():
        ks = R.sample(SHPS, 4)
        t = R.choice(ks)
        a = ks.index(t)
        pic = zh(K.lettered_shapes_svg([(k, R.choice(CLRS)) for k in ks]), "A到D四个图形")
        return mcq("哪一个是%s？%s" % (SHP[t], pic), LET[a], [x for i, x in enumerate(LET) if i != a], "%s 是%s。答案是 <b>%s</b>。" % (LET[a], SHP[t], LET[a]))
    return mk


def shape_count():
    def mk():
        n = R.randint(7, 12)
        items = [(R.choice(SHPS[:4]), R.choice(CLRS)) for _ in range(n)]
        if R.random() < 0.5:
            k = R.choice([x for x, _ in items])
            c = sum(1 for x, _ in items if x == k)
            q, unit_ = "有几个%s？" % SHP[k], "%s" % SHP[k]
        else:
            col = R.choice([y for _, y in items])
            c = sum(1 for _, y in items if y == col)
            q, unit_ = "%s的图形有几个？" % CLRN[col], "%s的" % CLRN[col]
        pic = zh(K.shapes_mix_svg(items, R.randint(1, 10 ** 6), 5, 3), "很多图形")
        return mcq(q + pic, "%d 个" % c, ["%d 个" % x for x in L.near(c, 0, 12) + [n]], "只数%s，一共 <b>%d 个</b>。" % (unit_, c))
    return mk


SFACT = [("三角形有几条边？", "3 条", ["4 条", "2 条", "5 条"]), ("三角形有几个角？", "3 个", ["4 个", "0 个", "6 个"]),
         ("正方形有几条边？", "4 条", ["3 条", "5 条", "6 条"]), ("长方形有几个角？", "4 个", ["3 个", "2 个", "6 个"]),
         ("圆形有几个角？", "0 个", ["1 个", "4 个", "3 个"]), ("六边形有几条边？", "6 条", ["5 条", "4 条", "8 条"]),
         ("哪种图形的 4 条边一样长？", "正方形", ["长方形", "三角形", "圆形"]), ("哪种图形没有角，能滚着走？", "圆形", ["三角形", "正方形", "长方形"]),
         ("两个一样的三角形能拼成什么？（沿长边拼）", "长方形", ["圆形", "六边形", "球"]), ("两个一样的正方形并排拼成什么？", "长方形", ["三角形", "圆形", "六边形"]),
         ("把正方形对折，沿着中间剪开，能得到什么？", "两个长方形", ["两个圆形", "两个六边形", "三个三角形"]),
         ("钟面的形状通常像什么图形？", "圆形", ["三角形", "正方形", "六边形"]), ("门的形状通常像什么图形？", "长方形", ["圆形", "三角形", "六边形"]),
         ("三明治斜着切一刀，每块像什么图形？", "三角形", ["圆形", "长方形", "六边形"])]


def shape_fact():
    pool = SFACT[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a, w = pool.pop()
        return mcq(q, a, w, "答案是<b>%s</b>。" % a)
    return mk


# ------------------------------------------------------------------ 分类和统计
CAT = {"水果": ["苹果", "香蕉", "梨", "桃子", "葡萄", "西瓜", "橘子", "草莓"],
       "动物": ["小猫", "小狗", "小兔", "老虎", "大象", "熊猫", "猴子", "长颈鹿"],
       "交通工具": ["汽车", "火车", "飞机", "轮船", "自行车", "公交车"],
       "文具": ["铅笔", "橡皮", "尺子", "蜡笔", "练习本", "卷笔刀"],
       "蔬菜": ["白菜", "萝卜", "黄瓜", "土豆", "茄子", "菠菜"],
       "衣服": ["裤子", "裙子", "毛衣", "外套", "衬衫", "T恤"]}


def odd_one():
    def mk():
        c1, c2 = R.sample(list(CAT), 2)
        xs = R.sample(CAT[c1], 3)
        o = R.choice(CAT[c2])
        ws = xs + [o]
        R.shuffle(ws)
        return mcq("%s，哪一个和其他三个不是一类？" % "、".join(ws), o, xs, "%s都是%s，<b>%s</b>是%s。" % ("、".join(xs), c1, o, c2))
    return mk


def cat_name():
    def mk():
        c = R.choice(list(CAT))
        xs = R.sample(CAT[c], 3)
        return mcq("%s都是什么？" % "、".join(xs), c, [x for x in CAT if x != c], "它们都是 <b>%s</b>。" % c)
    return mk


def sort_count():
    def mk():
        ks = R.sample(L.KINDS, 3)
        cs = [R.randint(2, 7) for _ in ks]
        if sum(cs) > 24:
            return None
        pic = zh(K.mixed_svg(list(zip(ks, cs)), R.randint(1, 10 ** 6)), "混在一起的东西")
        how = R.random()
        if how < 0.5:
            i = R.randrange(3)
            return mcq("先分一分，再数一数：%s有几%s？%s" % (nm(ks[i]), cl(ks[i]), pic), "%d%s" % (cs[i], cl(ks[i])),
                       ["%d%s" % (x, cl(ks[i])) for x in L.near(cs[i], 1, 12) + [sum(cs)]], "只数%s：<b>%d%s</b>。" % (nm(ks[i]), cs[i], cl(ks[i])))
        if len(set(cs)) < 3:
            return None
        most = how < 0.75
        t = max(cs) if most else min(cs)
        i = cs.index(t)
        return mcq("分一分，哪种东西最%s？%s" % ("多" if most else "少", pic), nm(ks[i]), [nm(k) for k in ks if k != ks[i]] + ["一样多"],
                   "%s，%s最%s：<b>%s</b>。" % ("、".join("%s %d" % (nm(k), c) for k, c in zip(ks, cs)), nm(ks[i]), "多" if most else "少", nm(ks[i])))
    return mk


def sort_rule():
    """按颜色分 / 按形状分 で何组"""
    def mk():
        ks = R.sample(SHPS[:4], R.randint(2, 4))
        cs = R.sample(CLRS, R.randint(2, 4))
        items = [(R.choice(ks), R.choice(cs)) for _ in range(R.randint(7, 11))]
        nk, nc = len({x for x, _ in items}), len({y for _, y in items})
        if nk == nc:
            return None
        by = R.choice(["形状", "颜色"])
        n = nk if by == "形状" else nc
        o = nc if by == "形状" else nk
        pic = zh(K.shapes_mix_svg(items, R.randint(1, 10 ** 6), 5, 3), "很多图形")
        return mcq("按%s分，可以分成几组？%s" % (by, pic), "%d 组" % n, ["%d 组" % x for x in (o, n + 1, n - 1, len(items)) if x > 0 and x != n],
                   "看%s：有 %s，分成 <b>%d 组</b>。" % (by, "、".join(sorted({SHP[x] for x, _ in items}) if by == "形状" else sorted({CLRN[y] for _, y in items})), n))
    return mk


def picto(kinds=("most", "less", "diff", "total", "one")):
    def mk():
        ks = R.sample(L.KINDS, 3)
        cs = R.sample(range(1, 9), 3)
        pic = zh(pictograph_svg(list(zip(ks, cs))), "统计图")
        how = R.choice(kinds)
        if how in ("most", "less"):
            t = max(cs) if how == "most" else min(cs)
            i = cs.index(t)
            return mcq("看统计图，哪种最%s？%s" % ("多" if how == "most" else "少", pic), nm(ks[i]), [nm(k) for k in ks if k != ks[i]] + ["一样多"],
                       "%s的一行最%s，有 %d%s。答案：<b>%s</b>。" % (nm(ks[i]), "长" if how == "most" else "短", t, cl(ks[i]), nm(ks[i])))
        if how == "one":
            i = R.randrange(3)
            return mcq("看统计图，%s有几%s？%s" % (nm(ks[i]), cl(ks[i]), pic), "%d%s" % (cs[i], cl(ks[i])),
                       ["%d%s" % (x, cl(ks[i])) for x in L.near(cs[i], 1, 10) + cs], "数%s那一行：<b>%d%s</b>。" % (nm(ks[i]), cs[i], cl(ks[i])))
        if how == "diff":
            i, j = (0, 1) if cs[0] > cs[1] else (1, 0)
            d = cs[i] - cs[j]
            return mcq("看统计图，%s比%s多几个？%s" % (nm(ks[i]), nm(ks[j]), pic), "%d 个" % d,
                       ["%d 个" % x for x in (d + 1, d - 1, cs[i], cs[j]) if x > 0 and x != d], "%d － %d ＝ <b>%d 个</b>。" % (cs[i], cs[j], d))
        tot = sum(cs)
        if tot > 20:
            return None
        return mcq("看统计图，三种东西一共有几个？%s" % pic, "%d 个" % tot, ["%d 个" % x for x in (tot + 1, tot - 1, max(cs), tot + 2)],
                   "%s ＝ <b>%d 个</b>。" % (" ＋ ".join(map(str, cs)), tot))
    return mk


# ------------------------------------------------------------------ 规律
def pat_num10():
    def mk():
        p = R.choice(["AB", "ABC", "AAB", "ABB", "AABB"])
        ns = R.sample(range(1, 10), len(set(p)))
        mp = {ch: ns[i] for i, ch in enumerate(sorted(set(p)))}
        Ln = len(p) * 2 + R.randint(0, len(p) - 1)
        seq = [mp[p[i % len(p)]] for i in range(Ln + 1)]
        return mcq("按规律填数：%s，（　）" % "，".join(str(x) for x in seq[:-1]), str(seq[-1]), [str(x) for x in ns if x != seq[-1]] + [str(seq[-1] + 1), str(seq[-1] - 1)],
                   "%s一组重复出现，所以填 <b>%d</b>。" % ("、".join(str(mp[c]) for c in p), seq[-1]))
    return mk


def pat_grow():
    def mk():
        st = R.choice([1, 1, 2])
        down = R.random() < 0.4
        a = R.randint(1, 10 - st * 4) if not down else R.randint(1 + st * 4, 10)
        sq = [a + (-st if down else st) * i for i in range(5)]
        p = R.randint(1, 4)
        shown = ["?" if i == p else str(x) for i, x in enumerate(sq)]
        ans = sq[p]
        return mcq("按规律排数字卡片，? 是几？%s" % zh(K.cards_svg(shown), "数字卡片"), str(ans),
                   [str(x) for x in (ans + 1, ans - 1, ans + 2, ans - 2) if 0 <= x and x != ans],
                   "一个比一个%s %d，? 是 <b>%d</b>。" % ("少" if down else "多", st, ans))
    return mk


def pat_make():
    """创造规律：哪一排是按 AB（或 ABB…）排的"""
    def mk():
        p = R.choice(["AB", "AAB", "ABB", "ABC"])
        ks = R.sample(L.KINDS, 3)
        mp = {ch: ks[i] for i, ch in enumerate("ABC")}
        good = [mp[p[i % len(p)]] for i in range(6)]
        n = len(p)

        def periodic(r):
            return all(r[t] == r[t - n] for t in range(n, 6))
        bads = []
        for _ in range(60):
            r = good[:]
            i, j = R.sample(range(6), 2)
            r[i], r[j] = r[j], r[i]
            if r != good and not periodic(r) and r not in bads:
                bads.append(r)
            if len(bads) == 3:
                break
        if len(bads) < 3:
            return None
        rows = bads + [good]
        R.shuffle(rows)
        a = rows.index(good)
        sp, rh = 44, 48
        s = []
        for i, r in enumerate(rows):
            y = 10 + i * rh + rh / 2
            s.append(text(18, y + 7, LET[i], 18, col=GREEN))
            for j, k in enumerate(r):
                s.append(K.obj(k, 50 + sp / 2 + j * sp, y, 15))
        pic = zh(svg_wrap(60 + 6 * sp, 20 + 4 * rh, "".join(s), "x"), "A到D四排东西")
        word = "、".join(nm(mp[c]) for c in p)
        return mcq("哪一排是“%s”一组、重复排的？%s" % (word, pic), LET[a], [x for i, x in enumerate(LET) if i != a],
                   "%s 排是 %s、%s……一直重复。答案是 <b>%s</b>。" % (LET[a], word, word, LET[a]))
    return mk


# ------------------------------------------------------------------ 単元
S_CNT = "感知和理解数、量及数量关系：在生活和游戏中手口一致地点数物体，说出总数，认读 10 以内（到 20）的数，能用数词描述事物的数量和顺序"
S_CMP = "感知和理解数、量及数量关系：通过一一对应或数数比较两组物体的多少；初步理解量的相对性"
S_OP = "感知和理解数、量及数量关系：借助实际情境和操作（如合并或拿取）理解“加”和“减”的实际意义；能通过实物操作或其它方法进行 10 以内的加减运算"
S_REL = "感知和理解数、量及数量关系：比较物体的长短、高矮、粗细、厚薄、轻重；初步理解量的相对性"
S_SHP = "感知形状与空间关系：认识常见的平面图形和立体图形，能用常见的几何形体有创意地拼搭或画出物体的造型"
S_POS = "感知形状与空间关系：能按语言指示或根据简单示意图正确取放物品；能辨别自己的左右，用上下、前后、左右描述物体的位置"
S_PAT = "初步感知生活中数学的有用和有趣：能发现事物简单的排列规律，并尝试创造新的排列规律"
S_DATA = "感知和理解数、量及数量关系：按物体的特征分类，能用简单的记录表、统计图等表示简单的数量关系"

UNITS = {}


def U(slug, **kw):
    UNITS[slug] = kw


U("counting-to-10", sort=1, dom="N", std=S_CNT, seed=90101,
  title="10以内的点数：数一数有几个", short="10以内的点数",
  meta="幼儿园大班数学“10以内的点数”练习题：看图数一数、十格图、哪一组正好有几个、数字和汉字、数的顺序，图多字少，100题在线练习，附可打印答案。",
  kb="手指一个一个点着数，最后一个数就是总数", ks="数过的做个记号，不重复、不遗漏。",
  body=lesson(["用手指<b>一个一个地点着数</b>：点一个，说一个数。",
               "数到最后一个时说的数，就是<b>一共有几个</b>。",
               "数字 0 表示一个也没有。数的顺序是 0、1、2……10，越往后越大。"],
              [("★★★★★★ 有几颗星星？", ["点着数：1、2、3、4、5、6。"], "6 颗"),
               ("7 后面的数是几？", ["7、8……"], "8")],
              [("漏数或重复数", "数过的用手按住或做个记号。"),
               ("嘴快手慢，手和嘴对不上", "点一个，才说一个数。"),
               ("最后又说一遍“一共 1、2、3……”", "最后数到的那个数就是总数。")]),
  faq=[("幼儿园大班要会数到几？", "《3-6岁儿童学习与发展指南》中，5～6岁的孩子能在生活中点数物体、说出总数。大班先熟练数到 10，再数到 20。"),
       ("在家怎么练习点数？", "吃饭时数碗筷、上楼时数台阶、收玩具时数积木。让孩子用手指点着数，最后问“一共几个”。")],
  spec=lambda: [("数一数", [(L.count_pic(1, 10), 20)]),
                ("十格图", [(L.tf_count(), 20)]),
                ("哪一组正好有几个", [(which_group(2, 9), 20)]),
                ("数字和汉字", [(num_word(), 20)]),
                ("数的顺序", [(L.seq_fill(0, 10), 10), (L.before_after(0, 10), 10)])])

U("numbers-to-20", sort=2, dom="N", std=S_CNT, seed=90102,
  title="认识20以内的数", short="20以内的数",
  meta="幼儿园大班数学“认识20以内的数”练习题：数一数、两个十格图、10 和几、数的顺序、比大小，图多字少，100题在线练习，附可打印答案。",
  kb="先数满 10 个，再接着往后数", ks="10 和 4 合起来是 14；14 后面是 15。",
  body=lesson(["数得多时，先数出 <b>10 个</b>放在一起，再接着数 11、12、13……",
               "两个十格图：第一个满了是 10，第二个有几个，就是“十几”。",
               "比大小：按顺序数，后数到的数大。"],
              [("一个满的十格图和 3 个点", ["10 后面接着数：11、12、13。"], "13"),
               ("16 和 19，哪个大？", ["16、17、18、19，19 在后面。"], "19")],
              [("14 写成 104", "10 和 4 合起来是 14，只写两个数字。"),
               ("数到 19 后不知道下一个", "19 后面是 20。"),
               ("看物体大就说数大", "比的是个数，不是东西的大小。")]),
  faq=[("幼儿园要学到 20 吗？", "大班孩子在生活中常会数到 20 左右，一年级上册正式学 11～20 各数的认识。先能数、能读就可以。"),
       ("怎么帮孩子理解“十几”？", "用 10 根吸管捆成一捆，再加几根单独的吸管，说说“一捆和 3 根是 13”。")],
  spec=lambda: [("数一数", [(L.count_pic(11, 20), 20)]),
                ("两个十格图", [(tf20(), 20)]),
                ("10 和几", [(ten_and(), 20)]),
                ("数的顺序", [(L.seq_fill(0, 20), 10), (L.before_after(1, 20), 10)]),
                ("比大小", [(L.cmp_sym(0, 20), 10), (biggest(0, 20), 10)])])

U("counting-in-groups", sort=3, dom="N", std=S_CNT, seed=90103,
  title="按群数数：2个2个、5个5个地数", short="按群数数",
  meta="幼儿园大班数学“按群数数”练习题：2个2个地数、3个3个地数、5个5个地数、盘子里的东西一共几个、一双是两只，100题在线练习，附可打印答案。",
  kb="一组一组地数，比一个一个数快", ks="2、4、6、8、10 是 2 个 2 个地数；5、10、15、20 是 5 个 5 个地数。",
  body=lesson(["东西多的时候，可以<b>一组一组地数</b>。",
               "每组 2 个：2、4、6、8、10……每组 5 个：5、10、15、20。",
               "一双鞋是 2 只，一双筷子是 2 根，也可以 2 个 2 个地数。"],
              [("4 组，每组 2 个苹果", ["2、4、6、8"], "8 个"),
               ("3 盘，每盘 5 块饼干", ["5、10、15"], "15 块")],
              [("2 个 2 个数时，每次只加 1", "每次要多 2：2、4、6。"),
               ("数组数，忘了每组几个", "说出的数是一共有几个，不是有几组。"),
               ("5、10 后面说 11", "5 个 5 个地数：10 后面是 15。")]),
  faq=[("按群数数有什么用？", "能更快、更不容易出错地数出很多东西，也是以后学乘法（几个几）的基础。"),
       ("在家怎么练？", "收袜子时 2 只 2 只地数，数手指时 5 个 5 个地数（一只手 5 个，两只手 10 个）。")],
  spec=lambda: [("2个2个地数", [(group_count(2), 20)]),
                ("3个3个地数", [(group_count(3), 20)]),
                ("5个5个地数", [(group_count(5), 6), (skip_seq((5,)), 14)]),
                ("盘子里有几个", [(plates(), 20)]),
                ("一双和接着数", [(pairs(), 10), (skip_seq((2,)), 10)])])

U("comparing-quantities", sort=4, dom="N", std=S_CMP, seed=90104,
  title="比多少：一一对应比一比", short="比多少",
  meta="幼儿园大班数学“比多少”练习题：哪种多、哪一组最多最少、多几个少几个、排得长不一定多、比大小、生活中的比多少，100题在线练习，附可打印答案。",
  kb="一个对一个，有剩下的那一边多", ks="比多少要数个数，不看东西大小，也不看排得长不长。",
  body=lesson(["把两种东西<b>一个对一个</b>地排好，有剩下的那一种<b>多</b>。",
               "剩下几个，就是<b>多几个</b>；另一种就少几个。",
               "排得长、东西大，不一定多。一定要数一数，或者一个对一个比。"],
              [("苹果 6 个，星星 4 个", ["一个对一个，苹果剩下 2 个。"], "苹果多 2 个"),
               ("下面一行排得很宽，有 5 个；上面一行挤在一起，有 7 个", ["数一数：7 比 5 大。"], "上面多")],
              [("看哪一行长就说哪一行多", "数个数，或者一个对一个连线。"),
               ("多几个答成一共几个", "只数剩下的部分。"),
               ("把“少几个”和“多几个”分不清", "少几个和多几个是同一个数。")]),
  faq=[("为什么先学一一对应？", "不用数数也能比出多少，是理解数的大小和减法（多几、少几）的基础。"),
       ("在家怎么练？", "摆碗和筷子：一个碗配一双筷子，看看哪个多、多几个。")],
  spec=lambda: [("哪种多", [(L.cmp_more(1, 10), 20)]),
                ("哪一组最多、最少", [(most_group(), 20)]),
                ("多几个、少几个", [(more_by(), 20)]),
                ("排得长不一定多", [(cmp_trap(), 10), (L.cmp_sym(0, 10), 10)]),
                ("生活中的比多少", [(cmp_story(), 20)])])

U("ordinal-numbers", sort=5, dom="N", std=S_CNT, seed=90105,
  title="序数：第几个", short="序数",
  meta="幼儿园大班数学“序数”练习题：从左数、从右数第几个，第几和几个的区别，书架的第几层，排队第几，赛跑第几名，100题在线练习，附可打印答案。",
  kb="“几个”是数量，“第几”是位置", ks="先看从哪边开始数，再数到第几个。",
  body=lesson(["“第几”说的是<b>排在哪个位置</b>，“几个”说的是<b>一共有多少</b>。",
               "数第几之前，先看从<b>哪一边</b>开始：从左、从右、从上、从下、从前、从后。",
               "排队时，前面有 3 人，你就排第 4。"],
              [("一排 6 只小鸭，从左数第 3 只涂色，涂了几只？", ["“第 3 只”只有一只。"], "1 只"),
               ("小明前面有 2 人，他排第几？", ["2 人后面是小明。"], "第 3")],
              [("“第 4 个”涂了 4 个", "第 4 个只有一个。"),
               ("从右数却从左边开始数", "先找好开始的那一边。"),
               ("排第几时忘了算自己", "前面几人，再加自己。")]),
  faq=[("序数和基数有什么区别？", "基数表示有多少（5 个），序数表示排在第几（第 5 个）。大班孩子要能分清两者。"),
       ("生活中怎么练？", "排队、赛跑、爬楼梯时问一问“你排第几”“我们住第几层”。")],
  spec=lambda: [("从左、从右数第几", [(L.ord_row(), 20)]),
                ("第几和几个", [(L.ord_vs_count(), 20)]),
                ("书架的第几层", [(L.pos_shelf(("ord", "top")), 20)]),
                ("排队第几", [(queue_ord(), 20)]),
                ("赛跑第几名", [(race(), 20)])])

U("splitting-and-combining-numbers", sort=6, dom="N", std=S_OP, seed=90106,
  title="10以内数的分与合", short="分与合",
  meta="幼儿园大班数学“分与合”练习题：5以内和10以内的分与合、盒子里藏了几个、两只手各拿几个、凑满十格图，100题在线练习，附可打印答案。",
  kb="7 可以分成 3 和 4，3 和 4 合成 7", ks="分开的两部分合起来，就是原来的数。",
  body=lesson(["把一些东西<b>分成两份</b>，叫做分；把两份<b>合在一起</b>，叫做合。",
               "6 个糖分到两只手里：1 和 5、2 和 4、3 和 3……都合成 6。",
               "10 的分与合最常用：1 和 9、2 和 8、3 和 7、4 和 6、5 和 5。"],
              [("一共 8 个，外面有 5 个，盒子里有几个？", ["8 可以分成 5 和 3。"], "3 个"),
               ("十格图里有 6 个，还要几个才满？", ["数空格：4 个。"], "4 个")],
              [("分的时候把两部分都写成原来的数", "两部分都比原来的数小。"),
               ("凑 10 时数了有东西的格子", "要数空的格子。"),
               ("分法漏掉了", "按 1 和几、2 和几……有顺序地分。")]),
  faq=[("分与合为什么重要？", "它把“部分”和“整体”联系起来，是一年级学加法和减法的基础，凑十法也要用到。"),
       ("在家怎么玩？", "把 10 颗豆子藏在两只手里，打开一只手，让孩子猜另一只手里有几颗。")],
  spec=lambda: [("5以内的分与合", [(L.bond(5), 20)]),
                ("10以内的分与合", [(L.bond(10), 20)]),
                ("盒子里藏了几个", [(hidden(), 20)]),
                ("两只手各拿几个", [(hands(), 10), (L.bond_ways(), 10)]),
                ("凑满十格图", [(make10(), 20)])])

U("adding-and-taking-away", sort=7, dom="N", std=S_OP, seed=90107,
  title="10以内的加和减：合起来和拿走", short="合起来和拿走",
  meta="幼儿园大班数学“10以内的加和减”练习题：看图合起来、划掉的是拿走的、看图选算式、加法小故事、减法小故事，100题在线练习，附可打印答案。",
  kb="合起来变多，拿走变少", ks="又来了、又放进用加法；飞走了、吃掉了用减法。",
  body=lesson(["两部分<b>合起来</b>，东西变多了，这就是<b>加</b>：3 ＋ 2 ＝ 5。",
               "从里面<b>拿走</b>一些，东西变少了，这就是<b>减</b>：5 － 2 ＝ 3。",
               "可以用手指、积木摆一摆，再数一数结果。"],
              [("树上有 4 只鸟，又飞来 2 只", ["合起来：4 后面接着数 5、6。"], "6 只"),
               ("有 7 块饼干，吃了 3 块", ["拿走 3 块：7、6、5，剩 4 块。"], "4 块")],
              [("“飞走了”也用加法", "飞走、吃掉、拿走都是变少，用减法。"),
               ("接着数时又把第一个数数了一遍", "从下一个数开始数。"),
               ("把拿走的数当成剩下的数", "数没被划掉的。")]),
  faq=[("幼儿园要学加减算式吗？", "《指南》提出 5～6岁能借助合并、拿取理解加和减，能通过实物操作进行 10 以内的加减。先用实物和图，再认识 ＋、－、＝。"),
       ("孩子还在掰手指怎么办？", "很正常。多玩实物，慢慢就会记住常见的结果。")],
  spec=lambda: [("看图合起来", [(add_pic(), 20)]),
                ("划掉的是拿走的", [(take_pic(), 20)]),
                ("看图选算式", [(calc_pic(), 20)]),
                ("加法小故事", [(story("add"), 20)]),
                ("减法小故事", [(story("sub"), 20)])])

U("comparing-length-height-thickness-and-weight", sort=8, dom="N", std=S_REL, seed=90108,
  title="比较长短、高矮、粗细、厚薄和轻重", short="比长短高矮轻重",
  meta="幼儿园大班数学“量的比较”练习题：哪支铅笔最长、哪座积木塔最高、哪根最粗、哪本最厚、天平哪边重、量的相对性，100题在线练习，附可打印答案。",
  kb="比之前先把一头对齐", ks="同一个东西，和不同的东西比，可能长也可能短。",
  body=lesson(["比<b>长短</b>和<b>高矮</b>时，先把一头对齐，再看另一头。",
               "比<b>粗细</b>看宽窄，比<b>厚薄</b>看书平放时的高矮，比<b>轻重</b>可以用天平：重的一边往下沉。",
               "<b>量的相对性</b>：小明比小红高，却比爸爸矮。同一个人，和不同的人比，结果不一样。"],
              [("红绳比蓝绳长，蓝绳比黄绳长，哪根最长？", ["红 > 蓝 > 黄"], "红绳"),
               ("天平左边低下去了", ["重的一边往下沉。"], "左边重")],
              [("两头没对齐就比", "先对齐一头，再看另一头。"),
               ("大的一定重", "气球大却很轻，要称一称。"),
               ("中间的那个说是最长", "中间的比一个长，比另一个短。")]),
  faq=[("什么是量的相对性？", "一个东西的长短、高矮、轻重，要看和谁比。比如 B 比 A 长，又比 C 短。《指南》把它列为 5～6岁的目标。"),
       ("在家怎么练？", "全家比身高、比鞋子长短；用手掂一掂两样东西，猜一猜哪个重，再用秤称一称。")],
  spec=lambda: [("长短", [(longest(), 14), (offset_len(), 6)]),
                ("高矮", [(tallest(), 14), (tower_more(), 6)]),
                ("粗细和厚薄", [(thick(), 20)]),
                ("轻重", [(heavy(), 14), (life_cmp(), 6)]),
                ("量的相对性", [(relative(), 14), (life_cmp(), 6)])])

U("recognizing-shapes", sort=9, dom="G", std=S_SHP, seed=90109,
  title="认识图形：圆形、三角形、正方形、长方形", short="认识图形",
  meta="幼儿园大班数学“认识图形”练习题：认识圆形、三角形、正方形、长方形和六边形，找一找、数一数，图形的边和角，认识球、圆柱、正方体、长方体，100题在线练习，附可打印答案。",
  kb="看边和角，认出图形", ks="三角形 3 条边，正方形和长方形 4 条边，圆形没有角。",
  body=lesson(["<b>三角形</b>有 3 条边、3 个角；<b>正方形</b>有 4 条一样长的边；<b>长方形</b>有 4 条边，对边一样长。",
               "<b>圆形</b>圆圆的，没有边和角。<b>六边形</b>有 6 条边。",
               "认图形只看形状，不看颜色、大小和摆的方向。",
               "能立起来、拿在手里的是立体图形：球、圆柱、正方体、长方体。"],
              [("有 3 条边、3 个角的图形", ["数一数边。"], "三角形"),
               ("易拉罐像什么形状？", ["上下是圆，中间直直的。"], "圆柱")],
              [("斜着放的三角形就不认识了", "转一转，边和角的个数不变。"),
               ("把正方形叫成长方形", "4 条边一样长的是正方形。"),
               ("球和圆形分不清", "圆形是平的，球是立体的，能滚。")]),
  faq=[("大班要认识哪些图形？", "常见的平面图形（圆形、三角形、正方形、长方形等）和立体图形（球、圆柱、正方体、长方体），并能用它们拼搭造型。"),
       ("在家怎么练？", "找一找家里像圆形、长方形的东西；用积木拼房子，说说用了哪些形状。")],
  spec=lambda: [("这是什么图形", [(shape_name(), 20)]),
                ("找一找", [(which_shape(), 20)]),
                ("数一数", [(shape_count(), 20)]),
                ("边和角", [(shape_fact(), 14), (shape_name(), 6)]),
                ("立体图形", [(L.sol_name(), 10), (L.sol_obj(), 10)])])

U("position-and-direction", sort=10, dom="G", std=S_POS, seed=90110,
  title="位置和方向：上下、前后、左右", short="位置和方向",
  meta="幼儿园大班数学“位置和方向”练习题：上面和下面、前面和后面、左边和右边、九格图里找位置、辨别自己的左右，100题在线练习，附可打印答案。",
  kb="先找“谁的”，再说上下、前后、左右", ks="写字的手（大多数人）是右手；面对面时，对方的左右和你相反。",
  body=lesson(["说位置时，先说<b>以谁为准</b>：桌子的上面、箱子的后面。",
               "<b>上下</b>看高低；<b>前后</b>看谁挡住谁；<b>左右</b>看自己的左手和右手。",
               "按顺序找时，先看从哪边开始数。"],
              [("苹果被箱子挡住了一半", ["被挡住的在后面。"], "箱子后面"),
               ("一排：小鱼、星星、杯子。星星右边是什么？", ["从星星往右看一个。"], "杯子")],
              [("左右分不清", "右手腕上戴个小手环，常玩“举右手”的游戏。"),
               ("面对面时照搬左右", "对方的右手在你的左边。"),
               ("忘了说以谁为准", "要说“谁的”上面、后面。")]),
  faq=[("大班要会辨别左右吗？", "是的，《指南》提出 5～6岁能辨别自己的左右，能按语言指示或简单示意图正确取放物品。"),
       ("在家怎么练？", "收玩具时说“把小熊放在书架第二层的左边”，让孩子按指示放。")],
  spec=lambda: [("上面、下面、旁边", [(L.pos_table(), 20)]),
                ("前面、后面", [(L.pos_box(), 20)]),
                ("左边、右边", [(L.pos_lr(), 20)]),
                ("九格图", [(L.pos_grid(), 14), (L.pos_words(), 6)]),
                ("书架和自己的左右", [(L.pos_shelf(("top", "near")), 14), (L.pos_lr_body(), 6)])])

U("repeating-patterns", sort=11, dom="U", std=S_PAT, seed=90111,
  title="找规律：按规律接着排", short="找规律",
  meta="幼儿园大班数学“找规律”练习题：东西的规律、颜色的规律、图形的规律、中间缺了什么、数字的规律、哪一排是按规律排的，100题在线练习，附可打印答案。",
  kb="找出一组，看它怎样重复", ks="红、蓝、红、蓝……是“红、蓝”一组重复。",
  body=lesson(["先找出<b>重复的一组</b>：苹果、星星、苹果、星星……一组是“苹果、星星”。",
               "再按这一组接着往后排，或者补上中间缺的。",
               "数字也能有规律：1、2、1、2……或者 2、3、4、5……一个比一个多 1。"],
              [("红、红、蓝、红、红、蓝、红、红、（　）", ["一组是红、红、蓝。"], "蓝"),
               ("3、4、5、6、（　）", ["一个比一个多 1。"], "7")],
              [("只看最后一个就猜", "先找出一整组。"),
               ("“AAB”看成“AB”", "数一数一组里有几个。"),
               ("中间缺的照着前一个填", "从头按规律数到缺的地方。")]),
  faq=[("为什么要找规律？", "找规律是发现数学关系的开始。《指南》提出 5～6岁能发现简单的排列规律，并尝试创造新的规律。"),
       ("在家怎么玩？", "用串珠、积木、贴纸排出“红黄红黄”或“大小小大小小”，让孩子接着排，再请孩子自己出题。")],
  spec=lambda: [("东西的规律", [(L.pat("obj"), 20)]),
                ("颜色的规律", [(L.pat("color"), 20)]),
                ("图形的规律", [(L.pat("shape"), 20)]),
                ("中间缺了什么", [(L.pat_mid(), 14), (pat_make(), 6)]),
                ("数字的规律", [(pat_num10(), 10), (pat_grow(), 10)])])

U("sorting-and-recording", sort=12, dom="N", std=S_DATA, seed=90112,
  title="分类和记录：分一分、数一数", short="分类和记录",
  meta="幼儿园大班数学“分类和记录”练习题：哪一个不是一类、它们都是什么、分一分数一数、按颜色和形状分、看统计图，100题在线练习，附可打印答案。",
  kb="先定好按什么分，再分、再数", ks="按颜色分和按形状分，分出的组不一样。",
  body=lesson(["分类前先想好<b>按什么分</b>：按种类、按颜色、按形状、按大小。",
               "分好后，<b>一类一类地数</b>，再比一比哪一类多、哪一类少。",
               "把数出的结果画成<b>统计图</b>：一行一种东西，哪一行长，哪一种就多。"],
              [("苹果、香蕉、汽车、梨，哪一个不是一类？", ["苹果、香蕉、梨是水果。"], "汽车"),
               ("统计图里小鱼那一行最长", ["一行越长，个数越多。"], "小鱼最多")],
              [("一边分一边换标准", "从头到尾都按同一个标准分。"),
               ("数的时候把别的类也数进去", "一类一类地数，数完一类做个记号。"),
               ("看统计图只看图片大小", "要数一行有几个。")]),
  faq=[("分类和统计在大班学什么？", "能按一个标准分类，数出每一类有几个，并用简单的记录表、统计图表示，《指南》把它列为 5～6岁的目标。"),
       ("在家怎么练？", "整理衣服时按袜子、裤子、上衣分；整理玩具时按颜色分，再数一数每类有几个。")],
  spec=lambda: [("哪一个不是一类", [(odd_one(), 20)]),
                ("它们都是什么", [(cat_name(), 10), (odd_one(), 10)]),
                ("分一分、数一数", [(sort_count(), 20)]),
                ("按颜色、按形状分", [(sort_rule(), 10), (shape_count(), 10)]),
                ("看统计图", [(picto(), 20)])])


def build(slug):
    u = UNITS[slug]
    setup(random.Random(u["seed"]))
    sets = build_sets(u["spec"](), u["seed"])
    unit(G, slug, u["sort"], u["dom"], u["std"], u["title"], u["short"], u["meta"], u["kb"], u["ks"],
         u["body"], u["faq"], sets, u["seed"])


if __name__ == "__main__":
    import sys
    for s in (sys.argv[1:] or list(UNITS)):
        print(s)
        build(s)
