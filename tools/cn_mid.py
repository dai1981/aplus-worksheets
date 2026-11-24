# -*- coding: utf-8 -*-
"""
中国 二〜四年级の自前の問題：竖式加减、混合运算、倍的认识、位置与方向（东南西北）、数对、两位数乘两位数 など。
setup(R) してから使う。
"""
import random
import tw_pics as P
from ws_common import svg_wrap, text, fig, INK, GREEN, RED, FILL, line
from cn_common import mcq, Names

R = random.Random(0)
NM = Names(R)


def setup(rnd):
    global R, NM
    R = rnd
    NM = Names(rnd)


def vpic(a, b, op):
    import re
    return re.sub(r"aria-label='[^']*'", "aria-label='竖式'", P.col(a, b, op), count=1)


def _carries(a, b):
    c, n = 0, 0
    while a or b:
        if a % 10 + b % 10 + c >= 10:
            n, c = n + 1, 1
        else:
            c = 0
        a //= 10
        b //= 10
    return n


def _borrows(a, b):
    c, n = 0, 0
    while a:
        if a % 10 - c < b % 10:
            n, c = n + 1, 1
        else:
            c = 0
        a //= 10
        b //= 10
    return n


def no_carry_add(a, b):
    """進位を忘れた答え"""
    s, p = 0, 1
    while a or b:
        s += ((a % 10 + b % 10) % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return s


def no_borrow_sub(a, b):
    """大きい方から小さい方を引いた答え（退位を忘れる）"""
    s, p = 0, 1
    while a or b:
        s += abs(a % 10 - b % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return s


def vert(op, da, db, carry=None, story=False, mx=None):
    """竖式：op は ＋ か －。da, db はけた数。carry=True は進位（退位）あり、False はなし、None はどちらでも"""
    def mk():
        a = R.randint(10 ** (da - 1), 10 ** da - 1)
        b = R.randint(10 ** (db - 1), 10 ** db - 1)
        if op == "－" and b > a:
            a, b = b, a
        if op == "－" and a == b:
            return None
        k = _carries(a, b) if op == "＋" else _borrows(a, b)
        if carry is True and k == 0 or carry is False and k > 0:
            return None
        ans = a + b if op == "＋" else a - b
        if mx and ans > mx:
            return None
        wrong = no_carry_add(a, b) if op == "＋" else no_borrow_sub(a, b)
        cands = [wrong, ans + 10, ans - 10, ans + 1, ans - 1, ans + 100]
        if story:
            n = NM.next()
            if op == "＋":
                t = R.choice([("图书角原来有 %d 本书，又放进 %d 本。现在一共有多少本？", "本"),
                              ("学校买了 %d 个红气球和 %d 个蓝气球。一共买了多少个气球？", "个"),
                              ("%s上午走了 %d 步，下午走了 %d 步。一共走了多少步？", "步")])
                q = t[0] % ((n, a, b) if "%s" in t[0] else (a, b))
                u = t[1]
            else:
                t = R.choice([("果园里有 %d 棵树，砍掉了 %d 棵。还剩多少棵？", "棵"),
                              ("一本书有 %d 页，%s已经看了 %d 页。还剩多少页没看？", "页"),
                              ("车上有 %d 人，下车 %d 人。车上还有多少人？", "人")])
                q = t[0] % ((a, n, b) if "%s" in t[0] else (a, b))
                u = t[1]
            return mcq(q, "%d %s" % (ans, u), ["%d %s" % (x, u) for x in cands if x > 0],
                       "列式：%d %s %d ＝ <b>%d</b>（%s）。" % (a, op, b, ans, u))
        e = ("相同数位对齐，从个位加起，%s<b>%d</b>。" % ("满十向前一位进 1，" if k else "", ans) if op == "＋" else
             "相同数位对齐，从个位减起，%s<b>%d</b>。" % ("个位不够减，从十位退 1 当 10，" if k else "", ans))
        return mcq("用竖式计算：%d %s %d ＝ ？%s" % (a, op, b, vpic(a, b, op)), str(ans), [str(x) for x in cands if x >= 0], e)
    return mk


def chain(kind):
    """连加、连减、加减混合（100 以内）"""
    def mk():
        if kind == "add":
            a, b, c = R.randint(10, 40), R.randint(10, 30), R.randint(5, 30)
            ans = a + b + c
            q, e = "%d ＋ %d ＋ %d ＝ ？" % (a, b, c), "先算 %d ＋ %d ＝ %d，再算 %d ＋ %d ＝ <b>%d</b>。" % (a, b, a + b, a + b, c, ans)
            w = [a + b, ans + 10, ans - 10, ans + 1]
        elif kind == "sub":
            a = R.randint(60, 99)
            b, c = R.randint(10, 30), R.randint(5, 25)
            ans = a - b - c
            q, e = "%d － %d － %d ＝ ？" % (a, b, c), "从左往右：%d － %d ＝ %d，%d － %d ＝ <b>%d</b>。" % (a, b, a - b, a - b, c, ans)
            w = [a - b, a - b + c, ans + 10, ans - 1]
        else:
            a = R.randint(30, 80)
            b, c = R.randint(10, 30), R.randint(5, 30)
            if R.random() < 0.5:
                ans = a - b + c
                q, e = "%d － %d ＋ %d ＝ ？" % (a, b, c), "从左往右：%d － %d ＝ %d，%d ＋ %d ＝ <b>%d</b>。" % (a, b, a - b, a - b, c, ans)
                w = [a - b - c, a - (b + c), ans + 10, ans - 10]
            else:
                ans = a + b - c
                q, e = "%d ＋ %d － %d ＝ ？" % (a, b, c), "从左往右：%d ＋ %d ＝ %d，%d － %d ＝ <b>%d</b>。" % (a, b, a + b, a + b, c, ans)
                w = [a + b + c, ans + 10, ans - 10, ans + 1]
        if ans <= 0 or ans > 100:
            return None
        return mcq(q, str(ans), [str(x) for x in w if x >= 0], e)
    return mk


def mixed_ops(level=2):
    """二年级：乘加、乘减、除加、带小括号（100 以内）"""
    def mk():
        k = R.choice(["ma", "ms", "da", "pa", "pd"])
        if k == "ma":
            a, b, c = R.randint(2, 9), R.randint(2, 9), R.randint(5, 40)
            ans = c + a * b
            q = "%d ＋ %d × %d ＝ ？" % (c, a, b)
            w = [(c + a) * b, c + a + b, ans + 1, ans - 10]
            e = "先算乘法 %d × %d ＝ %d，再算 %d ＋ %d ＝ <b>%d</b>。" % (a, b, a * b, c, a * b, ans)
        elif k == "ms":
            a, b = R.randint(2, 9), R.randint(2, 9)
            c = R.randint(a * b + 5, 90)
            ans = c - a * b
            q = "%d － %d × %d ＝ ？" % (c, a, b)
            w = [(c - a) * b, c - a - b, ans + 1, ans + 10]
            e = "先算乘法 %d × %d ＝ %d，再算 %d － %d ＝ <b>%d</b>。" % (a, b, a * b, c, a * b, ans)
        elif k == "da":
            b, q0 = R.randint(2, 9), R.randint(2, 9)
            a = b * q0
            c = R.randint(5, 40)
            ans = c + q0
            q = "%d ＋ %d ÷ %d ＝ ？" % (c, a, b)
            w = [(c + a) // b if (c + a) % b == 0 else c + a - b, c + a, ans + 1, ans - 1]
            e = "先算除法 %d ÷ %d ＝ %d，再算 %d ＋ %d ＝ <b>%d</b>。" % (a, b, q0, c, q0, ans)
        elif k == "pa":
            a, b, c = R.randint(10, 40), R.randint(5, 30), R.randint(2, 3)
            if (a + b) * c > 100:
                return None
            ans = (a + b) * c
            q = "（%d ＋ %d）× %d ＝ ？" % (a, b, c)
            w = [a + b * c, a + b + c, ans + 10, ans - 1]
            e = "先算小括号里的 %d ＋ %d ＝ %d，再算 %d × %d ＝ <b>%d</b>。" % (a, b, a + b, a + b, c, ans)
        else:
            c, q0 = R.randint(2, 9), R.randint(2, 9)
            s = c * q0
            b = R.randint(5, 40)
            a = s + b
            if a > 100:
                return None
            ans = q0
            q = "（%d － %d）÷ %d ＝ ？" % (a, b, c)
            w = [a - b // c if b % c == 0 else a - b - c, s, ans + 1, ans + 2]
            e = "先算小括号里的 %d － %d ＝ %d，再算 %d ÷ %d ＝ <b>%d</b>。" % (a, b, s, s, c, ans)
        if ans < 0:
            return None
        return mcq(q, str(ans), [str(x) for x in w if x >= 0], e)
    return mk


def order_rule():
    S = [("算式 30 ＋ 5 × 4 应该先算哪一步？", "5 × 4", ["30 ＋ 5", "30 ＋ 4", "从左往右都一样"]),
         ("算式 48 － 6 ÷ 2 应该先算哪一步？", "6 ÷ 2", ["48 － 6", "48 ÷ 2", "从左往右都一样"]),
         ("算式（20 － 8）× 3 应该先算哪一步？", "20 － 8", ["8 × 3", "20 × 3", "从左往右都一样"]),
         ("算式 40 － 12 ＋ 8 应该先算哪一步？", "40 － 12", ["12 ＋ 8", "40 ＋ 8", "先算加法"]),
         ("算式 36 ÷ 4 × 2 应该先算哪一步？", "36 ÷ 4", ["4 × 2", "36 × 2", "先算乘法"]),
         ("算式 7 × 8 － 20 应该先算哪一步？", "7 × 8", ["8 － 20", "7 － 20", "从右往左"]),
         ("把 24 ÷ 4 ＝ 6 和 6 ＋ 15 ＝ 21 合成一个综合算式。", "15 ＋ 24 ÷ 4", ["（15 ＋ 24）÷ 4", "24 ÷ 4 ＋ 6", "15 ＋ 24 ＋ 4"]),
         ("把 35 － 15 ＝ 20 和 20 ÷ 5 ＝ 4 合成一个综合算式。", "（35 － 15）÷ 5", ["35 － 15 ÷ 5", "35 ÷ 5 － 15", "35 － 20 ÷ 5"]),
         ("把 6 × 7 ＝ 42 和 50 － 42 ＝ 8 合成一个综合算式。", "50 － 6 × 7", ["（50 － 6）× 7", "6 × 7 － 50", "50 － 42 × 7"]),
         ("把 18 ＋ 22 ＝ 40 和 40 ÷ 8 ＝ 5 合成一个综合算式。", "（18 ＋ 22）÷ 8", ["18 ＋ 22 ÷ 8", "18 ÷ 8 ＋ 22", "22 ÷ 8 ＋ 18"])]
    pool = S[:]
    R.shuffle(pool)

    def mk():
        if not pool:
            return None
        q, a, w = pool.pop()
        return mcq(q, a, w, "没有括号时先乘除、后加减；同一级的从左往右算；有小括号先算括号里的。答案是 <b>%s</b>。" % a)
    return mk


def mixed_story():
    def mk():
        n = NM.next()
        k = R.choice(range(4))
        if k == 0:
            a, b, c = R.randint(3, 9), R.randint(3, 9), R.randint(5, 30)
            q = "%s买了 %d 盒彩笔，每盒 %d 支，还有 %d 支散的。一共有多少支？" % (n, a, b, c)
            ans, ex = a * b + c, "%d × %d ＋ %d ＝ %d" % (a, b, c, a * b + c)
            w = [(a + b) * c if (a + b) * c < 200 else a + b + c, a * b, a * (b + c), ans + 1]
        elif k == 1:
            b, q0 = R.randint(2, 9), R.randint(2, 9)
            a = b * q0
            c = R.randint(1, q0 - 1) if q0 > 1 else 1
            q = "有 %d 个苹果，平均放进 %d 个盘子，每盘放几个？%s从一盘里拿走 %d 个，这盘还剩几个？" % (a, b, n, c)
            ans, ex = q0 - c, "%d ÷ %d － %d ＝ %d" % (a, b, c, q0 - c)
            w = [q0, a - c, (a - c) // b if (a - c) % b == 0 else q0 + c, ans + 1]
        elif k == 2:
            a, b = R.randint(20, 50), R.randint(5, 20)
            c = R.randint(2, 4)
            if (a + b) * c > 100 or (a - b) <= 0:
                return None
            q = "%s有 %d 张贴纸，又得到 %d 张，然后平均分给 %d 个小朋友（正好分完）。每人分到几张？" % (n, a, b, c)
            if (a + b) % c:
                return None
            ans, ex = (a + b) // c, "（%d ＋ %d）÷ %d ＝ %d" % (a, b, c, (a + b) // c)
            w = [a + b // c if b % c == 0 else a + b, a + b, ans + 1, ans - 1]
        else:
            a, b = R.randint(3, 9), R.randint(3, 9)
            c = R.randint(a * b + 1, 80)
            q = "一种笔记本每本 %d 元，%s买了 %d 本，付了 %d 元。应找回多少元？" % (a, n, b, c)
            ans, ex = c - a * b, "%d － %d × %d ＝ %d" % (c, a, b, c - a * b)
            w = [(c - a) * b if 0 < (c - a) * b < 300 else c - a - b, a * b, c - a, ans + 10]
        if ans <= 0:
            return None
        return mcq(q, str(ans), [str(x) for x in w if x is not None and x > 0], "列综合算式：%s。答案是 <b>%d</b>。" % (ex, ans))
    return mk


# ------------------------------------------------------------------ 倍的认识（三年级上）
THINGS = [("红花", "黄花", "朵"), ("苹果", "梨", "个"), ("小鸡", "小鸭", "只"), ("跳绳", "皮球", "根"), ("故事书", "连环画", "本"),
          ("白兔", "灰兔", "只"), ("彩笔", "铅笔", "支"), ("男生", "女生", "人")]


def times_pic():
    import k_pics as K
    def mk():
        k1, k2 = R.sample(["apple", "star", "ball", "flower", "duck", "fish", "heart", "cup"], 2)
        a = R.randint(2, 4)
        t = R.randint(2, 5)
        b = a * t
        import cn_low
        pic = cn_low.zh(K.match_svg([(a, k1, "", None), (b, k2, "", None)]), "两行东西")
        n1, n2 = cn_low.nm(k1), cn_low.nm(k2)
        return mcq("第二行的%s是第一行%s的几倍？%s" % (n2, n1, pic), "%d 倍" % t, ["%d 倍" % x for x in (b, b - a, t + 1, t - 1) if x > 0],
                   "把 %d 个看作一份，%d 里面有 %d 个 %d，所以是 <b>%d 倍</b>。" % (a, b, t, a, t))
    return mk


def times_find(kind):
    def mk():
        x, y, u = R.choice(THINGS)
        a = R.randint(2, 9)
        t = R.randint(2, 9)
        if kind == "howmany":
            b = a * t
            return mcq("有 %d %s%s，%s有 %d %s。%s的数量是%s的几倍？" % (a, u, x, y, b, u, y, x), "%d 倍" % t,
                       ["%d 倍" % v for v in (b - a, t + 1, t - 1, b + a) if v > 0],
                       "求一个数是另一个数的几倍，用除法：%d ÷ %d ＝ <b>%d</b>（倍）。" % (b, a, t))
        if kind == "times":
            b = a * t
            return mcq("有 %d %s%s，%s的数量是%s的 %d 倍。%s有多少%s？" % (a, u, x, y, x, t, y, u), "%d %s" % (b, u),
                       ["%d %s" % (v, u) for v in (a + t, b + a, b - a, b + t) if v > 0],
                       "求一个数的几倍是多少，用乘法：%d × %d ＝ <b>%d</b>（%s）。" % (a, t, b, u))
        b = a * t
        return mcq("%s有 %d %s，是%s的 %d 倍。%s有多少%s？" % (y, b, u, x, t, x, u), "%d %s" % (a, u),
                   ["%d %s" % (v, u) for v in (b * t if b * t < 500 else b + t, b - t, a + 1, a - 1) if v > 0],
                   "%s是 %d 份，%s是 1 份：%d ÷ %d ＝ <b>%d</b>（%s）。" % (y, t, x, b, t, a, u))
    return mk


# ------------------------------------------------------------------ 位置与方向（东南西北）
DIRS8 = {"北": (0, -1), "南": (0, 1), "东": (1, 0), "西": (-1, 0), "东北": (1, -1), "西北": (-1, -1), "东南": (1, 1), "西南": (-1, 1)}
PLACES = ["学校", "图书馆", "公园", "医院", "超市", "邮局", "书店", "电影院", "体育馆", "少年宫", "银行", "动物园"]


def map_svg(center, around, eight=False):
    """center を中心に、around = {方向: 場所}。北が上"""
    W = H = 300
    cx, cy, d = 150, 150, 95
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='8' fill='#fafaf5' stroke='%s'/>" % (W - 2, H - 2, GREEN)]
    s.append("<line x1='272' y1='52' x2='272' y2='18' stroke='%s' stroke-width='2.5'/>" % INK)
    s.append("<polygon points='272,12 266,26 278,26' fill='%s'/>" % INK)
    s.append(text(272, 66, "北", 14))
    s.append("<rect x='%d' y='%d' width='76' height='30' rx='6' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx - 38, cy - 15, FILL, GREEN))
    s.append(text(cx, cy + 6, center, 15))
    for dname, place in around.items():
        dx, dy = DIRS8[dname]
        x, y = cx + dx * d, cy + dy * d
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#bbb' stroke-width='2' stroke-dasharray='4 4'/>" % (cx + dx * 40, cy + dy * 18, x - dx * 34, y - dy * 14))
        s.append("<rect x='%.1f' y='%.1f' width='68' height='28' rx='6' fill='#fff' stroke='%s' stroke-width='1.4'/>" % (x - 34, y - 14, INK))
        s.append(text(x, y + 6, place, 14))
    return fig(svg_wrap(W, H, "".join(s), "%s和周围的地方（上北下南）" % center))


def dir_map(eight=False):
    def mk():
        ds = list(DIRS8) if eight else ["北", "南", "东", "西"]
        k = min(len(ds), R.randint(4, 6) if eight else 4)
        chosen = R.sample(ds, k)
        pl = R.sample(PLACES, k + 1)
        center = pl[0]
        around = dict(zip(chosen, pl[1:]))
        d = R.choice(chosen)
        if R.random() < 0.5:
            return mcq("%s在%s的哪个方向？%s" % (around[d], center, map_svg(center, around)), d + "面",
                       [x + "面" for x in R.sample([x for x in ds if x != d], 3)],
                       "地图上通常是上北下南、左西右东。%s在%s的<b>%s面</b>。" % (around[d], center, d))
        return mcq("%s的%s面是什么地方？%s" % (center, d, map_svg(center, around)), around[d],
                   [around[x] for x in chosen if x != d] + R.sample([p for p in PLACES if p not in pl], 2),
                   "上北下南、左西右东，%s面是<b>%s</b>。" % (d, around[d]))
    return mk


def dir_opp():
    OPP = {"东": "西", "西": "东", "南": "北", "北": "南", "东北": "西南", "西南": "东北", "西北": "东南", "东南": "西北"}

    def mk():
        a, b = R.sample(PLACES, 2)
        d = R.choice(list(OPP))
        return mcq("%s在%s的%s面，那么%s在%s的哪一面？" % (a, b, d, b, a), OPP[d] + "面",
                   [x + "面" for x in R.sample([x for x in OPP if x not in (d, OPP[d])], 2)] + [d + "面"],
                   "方向是相对的：A 在 B 的%s面，B 就在 A 的<b>%s面</b>。" % (d, OPP[d]))
    return mk


def dir_turn():
    ORDER = ["北", "东", "南", "西"]
    S = [("早晨，你面对太阳站着，你的前面是什么方向？", "东", ["西", "南", "北"], "太阳从东方升起，面对太阳就是面向<b>东</b>。"),
         ("早晨面对太阳站着，你的背后是什么方向？", "西", ["东", "南", "北"], "面向东，背后是<b>西</b>。"),
         ("早晨面对太阳站着，你的左手边是什么方向？", "北", ["南", "东", "西"], "面向东时，左边是<b>北</b>，右边是南。"),
         ("早晨面对太阳站着，你的右手边是什么方向？", "南", ["北", "东", "西"], "面向东时，右边是<b>南</b>。"),
         ("傍晚，太阳在哪个方向落下？", "西", ["东", "南", "北"], "太阳东升<b>西</b>落。"),
         ("地图上通常怎么规定方向？", "上北下南，左西右东", ["上南下北，左东右西", "上东下西，左北右南", "没有规定"], "地图通常是<b>上北下南，左西右东</b>。"),
         ("在北的右边、东的上面的方向叫什么？", "东北", ["西北", "东南", "西南"], "北和东之间是<b>东北</b>。"),
         ("在南和西之间的方向叫什么？", "西南", ["东南", "西北", "东北"], "南和西之间是<b>西南</b>。"),
         ("指南针红色的针一般指着哪个方向？", "南", ["北", "东", "西"], "“指南针”指着<b>南</b>（地图上用指北针，指向北）。")]
    pool = S[:]
    R.shuffle(pool)

    def mk():
        if pool and R.random() < 0.6:
            q, a, w, e = pool.pop()
            return mcq(q, a, w, e)
        f = R.choice(ORDER)
        turn = R.choice(["向右转", "向左转", "向后转"])
        i = ORDER.index(f)
        a = ORDER[(i + {"向右转": 1, "向左转": -1, "向后转": 2}[turn]) % 4]
        return mcq("你面向%s站着，%s后，面向什么方向？" % (f, turn), a, [x for x in ORDER if x != a],
                   "按顺时针北、东、南、西。面向%s%s，面向<b>%s</b>。" % (f, turn, a))
    return mk


def dir_route():
    def mk():
        ds = ["北", "东", "南", "西"]
        steps = [(R.choice(ds), R.choice([100, 200, 300, 150, 250])) for _ in range(2)]
        if steps[0][0] == steps[1][0]:
            return None
        a, b, c = R.sample(PLACES, 3)
        q = "%s从%s出发，先向%s走 %d 米到%s，再向%s走 %d 米到%s。一共走了多少米？" % (NM.next(), a, steps[0][0], steps[0][1], b, steps[1][0], steps[1][1], c)
        t = steps[0][1] + steps[1][1]
        return mcq(q, "%d 米" % t, ["%d 米" % x for x in (abs(steps[0][1] - steps[1][1]), t + 100, t - 50, steps[1][1]) if x > 0],
                   "%d ＋ %d ＝ <b>%d 米</b>。" % (steps[0][1], steps[1][1], t))
    return mk


def kg_cmp():
    def mk():
        a = R.randint(1, 9)
        b = R.choice([a * 1000 + d for d in (-500, -200, 200, 500, 0)] + [R.randint(1, 9) * 100])
        A = a * 1000
        ok = ">" if A > b else "<" if A < b else "="
        return mcq("%d 千克 ○ %d 克，○ 里填什么？" % (a, b), ok, [x for x in (">", "<", "=", "＋") if x != ok],
                   "%d 千克 ＝ %d 克，%d 克 %s %d 克，填 <b>%s</b>。" % (a, A, A, ok, b, ok))
    return mk


# ------------------------------------------------------------------ 两位数乘两位数（三年级下）
def tens_mult():
    def mk():
        k = R.choice(["t", "h", "tt"])
        if k == "t":
            a, b = R.randint(11, 49), R.choice([10, 20, 30, 40])
            if a * b > 2000:
                return None
            ans = a * b
            q, e = "%d × %d ＝ ？" % (a, b), "先算 %d × %d ＝ %d，再在末尾添 1 个 0：<b>%d</b>。" % (a, b // 10, a * (b // 10), ans)
            w = [a * (b // 10), ans * 10, ans + 10, ans - 10]
        elif k == "h":
            a, b = R.randint(2, 9), R.choice([100, 200, 300]) // 100 * R.choice([10])
            a, b = R.randint(2, 9) * 10, R.randint(2, 9) * 10
            ans = a * b
            q, e = "%d × %d ＝ ？" % (a, b), "%d × %d ＝ %d，再添 2 个 0：<b>%d</b>。" % (a // 10, b // 10, a * b // 100, ans)
            w = [ans // 10, ans * 10, a * b // 100, ans + 100]
        else:
            a, b = R.randint(11, 30), R.randint(2, 4)
            ans = a * b * 10
            q, e = "%d × %d0 ＝ ？" % (a, b), "%d × %d ＝ %d，再添 1 个 0：<b>%d</b>。" % (a, b, a * b, ans)
            w = [a * b, ans * 10, ans + 10, ans - 10]
        return mcq(q, str(ans), [str(x) for x in w if x > 0], e)
    return mk


def two_by_two(carry):
    def mk():
        a, b = R.randint(11, 99), R.randint(11, 99)
        p1, p2 = a * (b % 10), a * (b // 10)
        has = a * (b % 10) >= 100 or any((a % 10) * d >= 10 for d in (b % 10, b // 10))
        if carry is False and has:
            return None
        ans = a * b
        w = [p1 + p2, p1 + p2 * 10 + 10, ans + 100, ans - 10]
        return mcq("用竖式计算：%d × %d ＝ ？%s" % (a, b, vpic_mul(a, b)), str(ans), [str(x) for x in w if x > 0],
                   "%d × %d ＝ %d，%d × %d0 ＝ %d，%d ＋ %d ＝ <b>%d</b>。" % (a, b % 10, p1, a, b // 10, p2 * 10, p1, p2 * 10, ans))
    return mk


def vpic_mul(a, b):
    import re
    return re.sub(r"aria-label='[^']*'", "aria-label='竖式'", P.col(a, b, "×"), count=1)


def two_by_two_est():
    def mk():
        a, b = R.randint(11, 99), R.randint(11, 99)
        ra, rb = int(round(a, -1)), int(round(b, -1))
        if ra == a and rb == b:
            return None
        est = ra * rb
        return mcq("估算：%d × %d 大约是多少？（把两个数都看成整十数）" % (a, b), "大约 %d" % est,
                   ["大约 %d" % x for x in (est + ra, est - rb, est * 10, a * b) if x > 0 and x != est],
                   "%d ≈ %d，%d ≈ %d，%d × %d ＝ <b>%d</b>，所以大约是 %d。" % (a, ra, b, rb, ra, rb, est, est))
    return mk


def two_by_two_story():
    S = [("每盒彩笔有 %d 支，学校买了 %d 盒。一共买了多少支？", "支"), ("每排坐 %d 人，礼堂有 %d 排。一共能坐多少人？", "人"),
         ("一本故事书 %d 元，班里买了 %d 本。一共要付多少元？", "元"), ("每箱苹果 %d 个，果园运来 %d 箱。一共多少个苹果？", "个"),
         ("小明每分钟走 %d 米，走了 %d 分钟。一共走了多少米？", "米"), ("一辆大巴车坐 %d 人，%d 辆大巴车一共能坐多少人？", "人")]

    def mk():
        t, u = R.choice(S)
        a, b = R.randint(12, 65), R.randint(12, 45)
        ans = a * b
        w = [a * (b % 10) + a * (b // 10), a + b, ans + 10, ans - a]
        return mcq(t % (a, b), "%d %s" % (ans, u), ["%d %s" % (x, u) for x in w if x > 0],
                   "%d × %d ＝ <b>%d</b>（%s）。" % (a, b, ans, u))
    return mk


def dec1_story():
    S = [("一支铅笔 %.1f 元，一块橡皮 %.1f 元。买这两样一共要多少元？", "元", "+"), ("一根绳子长 %.1f 米，剪去 %.1f 米，还剩多少米？", "米", "-"),
         ("小红跳远跳了 %.1f 米，小华跳了 %.1f 米。两人一共跳了多少米？", "米", "+"), ("一瓶水有 %.1f 升，喝了 %.1f 升，还剩多少升？", "升", "-")]

    def mk():
        t, u, op = R.choice(S)
        a, b = R.randint(11, 89) / 10, R.randint(11, 59) / 10
        if op == "-" and b >= a:
            a, b = b + 1, a
        ans = round(a + b, 1) if op == "+" else round(a - b, 1)
        if ans != int(ans) or True:
            pass
        def f(x):
            s = "%.1f" % x
            return s[:-2] if s.endswith(".0") else s
        if f(ans) == "%d" % int(ans) and "." not in f(ans):
            return None
        return mcq(t % (a, b), "%s %s" % (f(ans), u), ["%s %s" % (f(x), u) for x in (ans + 1, ans - 0.1 if ans > 0.1 else ans + 0.2, ans * 10, round(a + b if op == "-" else abs(a - b), 1)) if x > 0],
                   "小数点对齐：%s %s %s ＝ <b>%s</b>（%s）。" % (f(a), "＋" if op == "+" else "－", f(b), f(ans), u))
    return mk


# ------------------------------------------------------------------ 四年级
def ha_conv():
    def mk():
        k = R.choice(["ha2m", "m2ha", "km2ha", "ha2km", "cmp", "pick"])
        if k == "ha2m":
            a = R.randint(2, 30)
            return mcq("%d 公顷 ＝ ___ 平方米" % a, str(a * 10000), [str(a * x) for x in (1000, 100, 100000)],
                       "1 公顷 ＝ 10000 平方米，%d 公顷 ＝ <b>%d</b> 平方米。" % (a, a * 10000))
        if k == "m2ha":
            a = R.randint(2, 90)
            return mcq("%d 平方米 ＝ ___ 公顷" % (a * 10000), str(a), [str(a * 10), str(a * 100), str(a * 1000)],
                       "10000 平方米 ＝ 1 公顷，<b>%d</b> 公顷。" % a)
        if k == "km2ha":
            a = R.randint(2, 50)
            return mcq("%d 平方千米 ＝ ___ 公顷" % a, str(a * 100), [str(a * 10), str(a * 1000), str(a * 10000)],
                       "1 平方千米 ＝ 100 公顷，<b>%d</b> 公顷。" % (a * 100))
        if k == "ha2km":
            a = R.randint(2, 90)
            return mcq("%d 公顷 ＝ ___ 平方千米" % (a * 100), str(a), [str(a * 10), str(a * 100), str(a * 1000)],
                       "100 公顷 ＝ 1 平方千米，<b>%d</b> 平方千米。" % a)
        if k == "cmp":
            a = R.randint(1, 9)
            b = R.choice([a * 100 + d for d in (-50, 50, 0, 200)])
            ok = ">" if a * 100 > b else "<" if a * 100 < b else "="
            return mcq("%d 平方千米 ○ %d 公顷，○ 里填什么？" % (a, b), ok, [x for x in (">", "<", "=", "＋") if x != ok],
                       "%d 平方千米 ＝ %d 公顷，填 <b>%s</b>。" % (a, a * 100, ok))
        S = [("一个足球场的面积大约是 7000 ___。", "平方米"), ("学校的占地面积大约是 3 ___。", "公顷"), ("北京市的面积大约是 16410 ___。", "平方千米"),
             ("一间教室的面积大约是 60 ___。", "平方米"), ("一个大型公园的面积大约是 50 ___。", "公顷"), ("一个小岛的面积大约是 4 ___。", "平方千米"),
             ("一本数学书封面的面积大约是 4 ___。", "平方分米"), ("一张邮票的面积大约是 6 ___。", "平方厘米")]
        q, a = R.choice(S)
        return mcq(q + "填哪个单位最合适？", a, [x for x in ("平方米", "公顷", "平方千米", "平方厘米", "平方分米") if x != a][:3],
                   "想一想实际大小，用<b>%s</b>最合适。" % a)
    return mk


def ha_story():
    PL = ["农田", "果园", "茶园", "鱼塘", "苗圃", "草场", "菜地", "林场"]

    def mk():
        k = R.choice(["rect", "rect", "sq", "km", "sum"])
        p = R.choice(PL)
        if k == "rect":
            a, b = R.randint(2, 12) * 100, R.randint(1, 9) * 100
            s = a * b
            return mcq("一块长方形%s长 %d 米、宽 %d 米。它的面积是多少公顷？" % (p, a, b), "%d 公顷" % (s // 10000),
                       ["%d 公顷" % x for x in (s // 1000, (a + b) * 2 // 100, s // 100) if x != s // 10000] + ["%d 公顷" % (s // 10000 + 1)],
                       "%d × %d ＝ %d（平方米），%d ÷ 10000 ＝ <b>%d 公顷</b>。" % (a, b, s, s, s // 10000))
        if k == "sq":
            side = R.randint(1, 9) * 100
            s = side * side
            return mcq("一块正方形%s边长 %d 米，面积是多少公顷？" % (p, side), "%d 公顷" % (s // 10000),
                       ["%d 公顷" % x for x in (s // 1000, side * 4 // 100, s // 100, s // 10000 + 1) if x != s // 10000],
                       "%d × %d ＝ %d（平方米）＝ <b>%d 公顷</b>。" % (side, side, s, s // 10000))
        if k == "km":
            a = R.randint(2, 30)
            b = R.randint(10, 90)
            return mcq("一个湖的面积是 %d 平方千米，湖边的公园有 %d 公顷。湖的面积比公园大多少公顷？" % (a, b), "%d 公顷" % (a * 100 - b),
                       ["%d 公顷" % x for x in (a - b if a > b else b - a, a * 1000 - b, a * 10000 - b, a * 100 + b) if x > 0],
                       "%d 平方千米 ＝ %d 公顷，%d － %d ＝ <b>%d 公顷</b>。" % (a, a * 100, a * 100, b, a * 100 - b))
        a, b = R.randint(2, 20), R.randint(2, 20)
        c = R.randint(2, 9) * 1000
        return mcq("学校的%s有 %d 公顷，又开垦了 %d 平方米。现在一共有多少平方米？" % (p, a, c), "%d 平方米" % (a * 10000 + c),
                   ["%d 平方米" % x for x in (a + c, a * 1000 + c, a * 10000 + c * 10, a * 10000 - c)],
                   "%d 公顷 ＝ %d 平方米，%d ＋ %d ＝ <b>%d 平方米</b>。" % (a, a * 10000, a * 10000, c, a * 10000 + c))
    return mk


ANIMALS = [("鸡", "兔", 2, 4, "只"), ("鹤", "龟", 2, 4, "只"), ("自行车", "三轮车", 2, 3, "辆"), ("两人桌", "四人桌", 2, 4, "张")]


def cr(kind):
    def mk():
        a_, b_, la, lb, u = R.choice(ANIMALS[:2]) if kind != "car" else R.choice(ANIMALS[2:])
        x = R.randint(3, 20)
        y = R.randint(3, 20)
        n, legs = x + y, la * x + lb * y
        part = "腿" if "鸡" in a_ or "鹤" in a_ else ("轮子" if "车" in a_ else "座位")
        q = "%s和%s一共有 %d %s，%s一共有 %d 个。%s有多少%s？" % (a_, b_, n, u, part, legs, b_ if kind != "small" else a_, u)
        ans = y if kind != "small" else x
        e = ("假设全是%s：%d × %d ＝ %d（个），比实际少 %d － %d ＝ %d（个）。每把一%s%s换成%s多 %d 个，所以%s有 %d ÷ %d ＝ %d（%s）"
             % (a_, n, la, n * la, legs, n * la, legs - n * la, u, a_, b_, lb - la, b_, legs - n * la, lb - la, y, u))
        if kind == "small":
            e += "，%s有 %d － %d ＝ %d（%s）" % (a_, n, y, x, u)
        return mcq(q, "%d %s" % (ans, u), ["%d %s" % (v, u) for v in (n - ans, ans + 1, ans - 1, legs // lb, legs // la) if v > 0 and v != ans],
                   e + "。答案 <b>%d %s</b>。" % (ans, u))
    return mk


def cr_list():
    def mk():
        x, y = R.randint(1, 6), R.randint(1, 6)
        n, legs = x + y, 2 * x + 4 * y
        rows = "".join("<tr><td>%d</td><td>%d</td><td>%d</td></tr>" % (n - k, k, 2 * (n - k) + 4 * k) for k in range(0, n + 1))
        tb = "<div class='sn-tw'><table class='sn-table'><thead><tr><th>鸡（只）</th><th>兔（只）</th><th>腿（条）</th></tr></thead><tbody>%s</tbody></table></div>" % rows
        return mcq("鸡和兔一共 %d 只，腿一共 %d 条。用列表法找一找，兔有几只？%s" % (n, legs, tb), "%d 只" % y,
                   ["%d 只" % v for v in (x, y + 1, y - 1 if y > 1 else y + 2, n) if v != y],
                   "表中腿数是 %d 的那一行：鸡 %d 只、兔 <b>%d 只</b>。" % (legs, x, y))
    return mk


def dec_op(op, places=2, story=False):
    def f(x):
        s = ("%." + str(places) + "f") % x
        s = s.rstrip("0").rstrip(".") if "." in s else s
        return s

    def mk():
        k = 10 ** places
        a, b = R.randint(k + 1, 99 * k) / k, R.randint(11, 60 * k) / k
        if R.random() < 0.4:
            b = round(b, 1)
        if op == "-" and b >= a:
            a, b = b, a
        if a == b:
            return None
        ans = round(a + b if op == "+" else a - b, places)
        if ans <= 0:
            return None
        sa, sb = f(a), f(b)
        # 末尾を揃えずに計算した誤り：小数点の位置をずらす
        wrong = [ans + 1, ans + 0.1, ans - 0.01 if ans > 0.01 else ans + 0.02, round(a + b if op == "-" else abs(a - b), places)]
        if story:
            S = [("妈妈买菜用了 %s 元，买水果用了 %s 元。一共用了多少元？", "元", "+"), ("一根绳子长 %s 米，用去 %s 米，还剩多少米？", "米", "-"),
                 ("小明身高 %s 米，爸爸比他高 %s 米。爸爸身高多少米？", "米", "+"), ("一袋米重 %s 千克，吃了 %s 千克，还剩多少千克？", "千克", "-")]
            t = [x for x in S if x[2] == op]
            t, u, _ = R.choice(t)
            return mcq(t % (sa, sb), "%s %s" % (f(ans), u), ["%s %s" % (f(x), u) for x in wrong if x > 0],
                       "小数点对齐：%s %s %s ＝ <b>%s</b>（%s）。" % (sa, "＋" if op == "+" else "－", sb, f(ans), u))
        return mcq("%s %s %s ＝ ？" % (sa, "＋" if op == "+" else "－", sb), f(ans), [f(x) for x in wrong if x > 0],
                   "把小数点对齐，相同数位对齐再算：<b>%s</b>。" % f(ans))
    return mk


def dec_simplify():
    def mk():
        k = R.choice(["drop", "same", "write"])
        if k == "drop":
            a = R.randint(1, 99)
            s = "%d.%d0" % (a // 10, a % 10) if a % 10 else "%d.%d00" % (a // 10, R.randint(1, 9))
            v = s.rstrip("0").rstrip(".")
            return mcq("根据小数的性质，把 %s 化简。" % s, v, [s.replace(".", ""), v + "0" if s.count("0") > 1 else v + "1", "%d" % int(float(s))],
                       "小数的末尾去掉 0，大小不变：<b>%s</b>。" % v)
        if k == "same":
            a = R.randint(1, 9)
            return mcq("下面哪个数和 0.%d 相等？" % a, "0.%d0" % a, ["0.0%d" % a, "%d.0" % a, "0.%d1" % a],
                       "在小数末尾添上 0，大小不变：0.%d ＝ <b>0.%d0</b>。" % (a, a))
        a = R.randint(1, 99)
        return mcq("把 %d 改写成两位小数。" % a, "%d.00" % a, ["%d.0" % a, "0.%02d" % a if a < 100 else "%d.000" % a, "%d00" % a],
                   "在整数末尾点上小数点，再添两个 0：<b>%d.00</b>。" % a)
    return mk
