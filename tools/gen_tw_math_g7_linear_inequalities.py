# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：一元一次不等式（108課綱 A-7-7、A-7-8）
  python3 tools/gen_tw_math_g7_linear_inequalities.py
不等式の意味（＞・＜・≧・≦、「至少」「不超過」）、情境から列式、解く（負數で乘除すると不等號の向きが変わる）、數線上の表示（實心・空心）、應用（最多・最少の整數）。
誤答：負數で割っても向きを変えない、「至少」を＞にする、空心・實心を取り違える、最多 x 個で切り上げる。
"""
import random
from fractions import Fraction as F
from tw_common import ff, mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, INK, RED, num
from tw_g7 import sn, tidy_sets, term, const, lin

R = random.Random(71021)
NM = Names(R)
OPS = ["＞", "＜", "≧", "≦"]
FLIP = {"＞": "＜", "＜": "＞", "≧": "≦", "≦": "≧"}


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def ray(c, op):
    lo, hi = c - 5, c + 5
    W = 40 + 10 * 30
    X = lambda v: 20 + (v - lo) * 30
    s = [line(10, 40, W - 6, 40, INK, 2)]
    for v in range(lo, hi + 1):
        s.append(line(X(v), 34, X(v), 46, INK, 1.2))
        s.append(text(X(v), 62, sn(v), 11))
    right = op in ("＞", "≧")
    x0 = X(c)
    x1 = W - 10 if right else 12
    s.append("<line x1='%.0f' y1='22' x2='%.0f' y2='22' stroke='%s' stroke-width='3'/>" % (x0, x1, RED))
    s.append("<line x1='%.0f' y1='22' x2='%.0f' y2='40' stroke='%s' stroke-width='2'/>" % (x0, x0, RED))
    fill = RED if op in ("≧", "≦") else "#fff"
    s.append("<circle cx='%.0f' cy='22' r='5' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, fill, RED))
    return fig(svg_wrap(W, 70, "".join(s), "數線上的解"))


def s1(seen):
    W = [("x 至少是 %d", "x ≧ %d", ["x ＞ %d", "x ≦ %d", "x ＜ %d"]), ("x 不超過 %d", "x ≦ %d", ["x ＜ %d", "x ≧ %d", "x ＞ %d"]),
         ("x 比 %d 大", "x ＞ %d", ["x ≧ %d", "x ＜ %d", "x ≦ %d"]), ("x 小於 %d", "x ＜ %d", ["x ≦ %d", "x ＞ %d", "x ≧ %d"]),
         ("x 最多是 %d", "x ≦ %d", ["x ＜ %d", "x ≧ %d", "x ＞ %d"]), ("x 不少於 %d", "x ≧ %d", ["x ＞ %d", "x ≦ %d", "x ＜ %d"])]

    def mk():
        t, a, w = R.choice(W)
        k = R.randint(-20, 50)
        return mcq("「%s」用不等式表示是？" % (t % k), a % k, [x % k for x in w], "「至少、不少於」用 ≧；「不超過、最多」用 ≦；「大於、小於」不含等號。")

    def ctx():
        p, m = R.choice([25, 35, 45, 60]), R.choice([200, 300, 500])
        q = "一枝筆 %d 元，帶 %d 元去買 x 枝，錢夠用。哪一個不等式正確？" % (p, m)
        return mcq(q, "%dx ≦ %d" % (p, m), ["%dx ＜ %d" % (p, m), "%dx ≧ %d" % (p, m), "x ＋ %d ≦ %d" % (p, m)], "花的錢 %dx 不能超過 %d 元，可以剛好等於：%dx ≦ %d。" % (p, m, p, m))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, ctx, 8, seen)


def s2(seen):
    def mk():
        a = nz(-6, 6)
        b = nz(-12, 12)
        x0 = nz(-8, 8)
        c = a * x0 + b
        op = R.choice(OPS)
        res = op if a > 0 else FLIP[op]
        q = "解不等式：%s %s %s" % (lin(a, b), op, sn(c))
        ans = "x %s %s" % (res, sn(x0))
        return mcq(q, ans, ["x %s %s" % (FLIP[res], sn(x0)), "x %s %s" % (res, sn(-x0)), "x %s %s" % (res, sn(F(c + b, a))) if F(c + b, a) != x0 else "x %s %s" % (res, sn(x0 + 1))],
                   "移項：%s %s %s，%s%s。" % (term(a, "x", True), op, sn(c - b), "兩邊同除以 %s，不等號不變" % sn(a) if a > 0 else "兩邊同除以負數 %s，<b>不等號要反向</b>" % sn(a), "：" + ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        c = nz(-4, 4)
        op = R.choice(OPS)
        g = ray(c, op)
        ans = "x %s %s" % (op, sn(c))
        return mcq("數線上紅色部分表示哪一個不等式的解？" + g, ans, ["x %s %s" % (o, sn(c)) for o in OPS if o != op],
                   "%s，%s：%s。" % ("往右（比 %s 大）" % sn(c) if op in ("＞", "≧") else "往左（比 %s 小）" % sn(c), "實心點表示包含 %s" % sn(c) if op in ("≧", "≦") else "空心點表示不包含 %s" % sn(c), ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def ints():
        a = R.randint(2, 6)
        b = nz(-10, 10)
        c = R.randint(-10, 30)
        lim = F(c - b, a)
        op = R.choice(["＜", "≦"])
        import math
        if op == "＜":
            top = math.ceil(lim) - 1
        else:
            top = math.floor(lim)
        if top < 1:
            return None
        q = "滿足 %s %s %s 的<b>正整數</b> x 有幾個？" % (lin(a, b), op, sn(c))
        return mcq(q, "%d 個" % top, ["%d 個" % t for t in (top + 1, top - 1 if top > 1 else top + 2, math.floor(lim) + 1)  if t != top] + ["%d 個" % (top + 3)], "解得 x %s %s，正整數是 1 到 %d，共 %d 個。" % (op, ff(lim), top, top))

    def biggest():
        a = R.choice([2, 3, 4, 5, -2, -3])
        b = nz(-10, 10)
        c = R.randint(-15, 15)
        lim = F(c - b, a)
        import math
        if a > 0:
            v = math.ceil(lim) - 1 if lim.denominator == 1 else math.floor(lim)
            q = "滿足 %s ＜ %s 的最大整數是多少？" % (lin(a, b), sn(c))
            e = "x ＜ %s，最大整數是 %s。" % (sn(lim) if lim < 0 else ff(lim), sn(v))
        else:
            v = math.floor(lim) + 1 if lim.denominator == 1 else math.ceil(lim)
            q = "滿足 %s ＜ %s 的最小整數是多少？" % (lin(a, b), sn(c))
            e = "除以負數不等號反向：x ＞ %s，最小整數是 %s。" % (sn(lim), sn(v))
        return mcq(q, sn(v), [sn(v + 1), sn(v - 1), sn(-v) if v else "1"], e)
    return pick_unique(R, ints, 10, seen) + pick_unique(R, biggest, 10, seen)


def s5(seen):
    def buy():
        p = R.choice([35, 45, 55, 65, 85])
        fee = R.choice([0, 50, 60, 100])
        m = R.choice([500, 800, 1000])
        n = (m - fee) // p
        q = "%s帶 %d 元，先付 %d 元入場費，剩下的錢買每個 %d 元的紀念品，最多可以買幾個？" % (NM.next(), m, fee, p) if fee else "%s帶 %d 元，買每個 %d 元的紀念品，最多可以買幾個？" % (NM.next(), m, p)
        return mcq(q, "%d 個" % n, ["%d 個" % t for t in (n + 1, m // p if m // p != n else n - 1, n - 1)  if t != n] + ["%d 個" % (n + 2)], "%s%dx ≦ %d，x ≦ %s，最多 %d 個（只能取整數，要捨去）。" % ("%d ＋ " % fee if fee else "", p, m, ff(F(m - fee, p)), n))

    def score():
        n = R.choice([3, 4])
        avg = R.choice([80, 85, 90])
        got = [R.randint(70, 95) for _ in range(n - 1)]
        need = avg * n - sum(got)
        if need > 100 or need < 50:
            return None
        q = "%s前 %d 次考試是 %s 分，想讓 %d 次平均至少 %d 分，最後一次至少要考幾分？" % (NM.next(), n - 1, "、".join(map(str, got)), n, avg)
        return mcq(q, "%d 分" % need, ["%d 分" % t for t in (avg, need + 1, need - 1)  if t != need], "（%s ＋ x）÷ %d ≧ %d，x ≧ %d × %d － %d ＝ %d。" % (" ＋ ".join(map(str, got)), n, avg, avg, n, sum(got), need))

    def taxi():
        base, per, step = 85, 5, 200
        m = R.choice([200, 250, 300, 350])
        k = (m - base) // per
        q = "計程車起跳 85 元，之後每 200 公尺加 5 元。身上有 %d 元，最多可以跳表幾次（起跳後）？" % m
        return mcq(q, "%d 次" % k, ["%d 次" % t for t in (k + 1, m // per, k - 1)], "85 ＋ 5x ≦ %d，x ≦ %s，最多 %d 次。" % (m, ff(F(m - base, per)), k))
    return pick_unique(R, buy, 8, seen) + pick_unique(R, score, 8, seen) + pick_unique(R, taxi, 4, seen)


def main():
    seen = set()
    sets = [("寫出不等式", s1(seen)), ("解不等式", s2(seen)), ("在數線上表示", s3(seen)),
            ("整數解", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["不等號：＞ 大於、＜ 小於、<b>≧ 大於或等於（至少、不少於）</b>、<b>≦ 小於或等於（最多、不超過）</b>。",
         "解法和方程式一樣可以移項，但<b>兩邊同乘或同除以負數，不等號要反向</b>。",
         "數線：≧、≦ 用<b>實心點</b>（包含），＞、＜ 用<b>空心點</b>（不包含）。",
         "應用題的答案常要取整數：「最多」要捨去，「至少」要進位。"],
        [example("－3x ＋ 5 ≦ 17", ["移項：－3x ≦ 12。", "同除以 －3，不等號反向。"], "x ≧ －4"),
         example("帶 500 元買 45 元的東西，最多幾個？", ["45x ≦ 500，x ≦ 11.1…。"], "11 個")],
        [("－2x ＞ 6 解成 x ＞ －3", "除以負數要反向：x ＜ －3"),
         ("「至少 60 分」寫成 x ＞ 60", "至少包含 60：x ≧ 60"),
         ("x ≦ 11.1，答 12 個", "最多只能 11 個")])
    faq = [{"q": "為什麼乘以負數不等號要反向？",
            "a": "例如 2 ＜ 5，兩邊乘以 －1 變成 －2 和 －5，而 －2 ＞ －5，大小關係反過來了。"},
           {"q": "數線上的實心點和空心點有什麼不同？",
            "a": "實心點表示這個數也是解（≧、≦），空心點表示這個數不是解（＞、＜）。"},
           {"q": "七年級的一元一次不等式要學什麼？",
            "a": "108課綱 A-7-7、A-7-8：不等式的意義、在具體情境中列出一元一次不等式、解單一的一元一次不等式、在數線上標示解的範圍和應用問題。"}]
    make_unit(R, "grade-7", "linear-inequalities", "A-7-8",
              "一元一次不等式的解與應用：單一的一元一次不等式的解；在數線上標示解的範圍；應用問題。",
              "一元一次不等式",
              "七年級數學 一元一次不等式 練習題｜不等號反向・數線・整數解 學習單（附解答）",
              "一元一次不等式",
              "國中七年級數學「一元一次不等式」免費學習單：用不等式表示至少、不超過，解不等式（除以負數要反向）、在數線上表示解、整數解與買東西、平均分數應用題。100題線上練習馬上對答案，附可列印解答。",
              "同乘或同除以負數，不等號要反向",
              "≧、≦ 用實心點，＞、＜ 用空心點。",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
