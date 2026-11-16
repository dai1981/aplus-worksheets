# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：除法（108課綱 N-3-4）
  python3 tools/gen_tw_math_g3_division.py
除法的意義（平分・包含）、九九範圍的除法、有餘數的除法（餘數比除數小）、驗算、應用問題（多一輛車）。
餘數は台灣の書き方「29 ÷ 4 ＝ 7……1」。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, GREEN, FILL, INK

R = random.Random(31004)


def qr(q, r):
    return "%d……%d" % (q, r) if r else str(q)


def dots(total, group):
    """total 個を group 個ずつ並べた絵（包含除の手がかり）"""
    per_row = group
    rows = (total + per_row - 1) // per_row
    W, H = per_row * 26 + 20, rows * 30 + 14
    s = []
    for i in range(total):
        r, c = divmod(i, per_row)
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s' stroke='%s' stroke-width='2'/>" % (20 + c * 26, 20 + r * 30, FILL, GREEN))
    return fig(svg_wrap(W, H, "".join(s), "%d個圓，每排%d個" % (total, group)))


def s1(seen):
    nm = Names(R)

    def share():   # 等分除
        d, qv = R.randint(2, 9), R.randint(2, 9)
        n = d * qv
        thing = R.choice([("顆", "糖果"), ("張", "貼紙"), ("枝", "鉛筆"), ("本", "筆記本")])
        q = "%d %s%s平分給 %d 個人，每人分到幾%s？" % (n, thing[0], thing[1], d, thing[0])
        return mcq(q, "%d%s" % (qv, thing[0]), ["%d%s" % (x, thing[0]) for x in (n - d, n + d, qv + 1, qv - 1, d) if x > 0 and x != qv],
                   "平分用除法：%d ÷ %d ＝ %d（%s）。" % (n, d, qv, thing[0]))

    def group():   # 包含除
        g, qv = R.randint(2, 9), R.randint(2, 6)
        n = g * qv
        q = "%s有 %d 個橘子，每 %d 個裝一袋，可以裝幾袋？%s" % (nm.next(), n, g, dots(n, g) if n <= 30 else "")
        return mcq(q, "%d袋" % qv, ["%d袋" % x for x in (n - g, g, qv + 1, qv - 1, n + g) if x > 0 and x != qv],
                   "每 %d 個一袋，看 %d 裡有幾個 %d：%d ÷ %d ＝ %d（袋）。" % (g, n, g, n, g, qv))

    def mul_to_div():
        a, b = R.randint(2, 9), R.randint(2, 9)
        q = "因為 %d × %d ＝ %d，所以 %d ÷ %d ＝ ？" % (a, b, a * b, a * b, a)
        return mcq(q, str(b), [str(x) for x in (a, a * b, b + 1, b - 1, a + b) if x > 0 and x != b],
                   "乘除互逆：%d × %d ＝ %d，所以 %d ÷ %d ＝ %d。" % (a, b, a * b, a * b, a, b))
    return pick_unique(R, share, 8, seen) + pick_unique(R, group, 6, seen) + pick_unique(R, mul_to_div, 6, seen)


def fact(seen, n):
    def mk():
        d, qv = R.randint(2, 9), R.randint(2, 9)
        t = d * qv
        q = "%d ÷ %d ＝" % (t, d)
        return mcq(q, str(qv), [str(x) for x in (qv + 1, qv - 1, d, t - d, qv + 2) if x > 0 and x != qv],
                   "想九九：%d × ？＝ %d，%d × %d ＝ %d，所以答案是 %d。" % (d, t, d, qv, t, qv))
    return pick_unique(R, mk, n, seen)


def rem(seen, n):
    def mk():
        d = R.randint(2, 9)
        qv, r = R.randint(2, 9), R.randint(1, d - 1) if d > 1 else 0
        t = d * qv + r
        if r == 0 or t > 89:
            return None
        q = "%d ÷ %d ＝" % (t, d)
        w = [qr(qv - 1, r + d), qr(qv + 1, 0) if (qv + 1) * d - t < d else qr(qv + 1, r), qr(qv, r + 1) if r + 1 < d else qr(qv, r - 1),
             qr(qv - 1, r), qr(qv, d - r)]
        return mcq(q, qr(qv, r), [x for x in w if x != qr(qv, r)],
                   "%d × %d ＝ %d，%d － %d ＝ %d。餘數 %d 要比除數 %d 小，答案是 %s。" % (d, qv, d * qv, t, d * qv, r, r, d, qr(qv, r)))
    return pick_unique(R, mk, n, seen)


def s4(seen):
    def check():
        d = R.randint(3, 9)
        qv, r = R.randint(3, 9), R.randint(1, d - 1)
        t = d * qv + r
        q = "%s ÷ %d 的商是 %d，餘數是 %d。☐ 是多少？（☐ ÷ %d ＝ %d……%d）" % ("☐", d, qv, r, d, qv, r)
        return mcq(q, str(t), [str(x) for x in (d * qv, d * qv - r, (d + r) * qv, t + d, d + qv + r) if x > 0 and x != t],
                   "驗算：被除數 ＝ 除數 × 商 ＋ 餘數 ＝ %d × %d ＋ %d ＝ %d。" % (d, qv, r, t))

    def wrong():
        d = R.randint(3, 9)
        qv, r = R.randint(2, 8), R.randint(1, d - 1)
        t = d * qv + r
        bad = qr(qv - 1, r + d)
        q = "小明算 %d ÷ %d ＝ %s。哪裡錯了？" % (t, d, bad)
        right = "餘數 %d 比除數 %d 大，商還可以再大 1" % (r + d, d)
        return mcq(q, right, ["商太大了，要變小 1", "除數和被除數寫反了", "沒有錯，答案正確"],
                   "餘數一定要比除數小。%d ÷ %d ＝ %s。" % (t, d, qr(qv, r)))

    def max_rem():
        d = R.randint(3, 9)
        q = "一個數除以 %d，餘數最大可能是多少？" % d
        return mcq(q, str(d - 1), [str(x) for x in (d, d + 1, d - 2, 0 if d > 2 else 9)],
                   "餘數要比除數 %d 小，所以最大是 %d。" % (d, d - 1))
    return pick_unique(R, check, 9, seen) + pick_unique(R, wrong, 6, seen) + pick_unique(R, max_rem, 5, seen)


def s5(seen):
    nm = Names(R)

    def basic():
        d, qv, r = R.randint(3, 9), R.randint(3, 9), 0
        r = R.randint(1, d - 1)
        t = d * qv + r
        thing = R.choice([("顆", "彈珠", "個人"), ("張", "卡片", "個小朋友"), ("片", "餅乾", "個盤子")])
        q = "%d %s%s平分給 %d %s，每份最多幾%s？還剩下幾%s？" % (t, thing[0], thing[1], d, thing[2], thing[0], thing[0])
        a = "每份 %d %s，剩 %d %s" % (qv, thing[0], r, thing[0])
        w = ["每份 %d %s，剩 %d %s" % (qv - 1, thing[0], r + d, thing[0]),
             "每份 %d %s，剩 %d %s" % (qv + 1, thing[0], 0, thing[0]),
             "每份 %d %s，剩 %d %s" % (qv, thing[0], d - r, thing[0]) if d - r != r else "每份 %d %s，剩 %d %s" % (qv, thing[0], r + 1, thing[0])]
        return mcq(q, a, w, "%d ÷ %d ＝ %d……%d。" % (t, d, qv, r))

    def bus():   # 無條件進位
        d = R.randint(4, 9)
        qv, r = R.randint(3, 8), R.randint(1, d - 1)
        t = d * qv + r
        q = "%d 位小朋友去露營，每頂帳篷最多睡 %d 人。至少要幾頂帳篷？" % (t, d)
        return mcq(q, "%d頂" % (qv + 1), ["%d頂" % x for x in (qv, qv + 2, r, d)],
                   "%d ÷ %d ＝ %d……%d，剩下的 %d 人也要睡，所以要再多 1 頂：%d 頂。" % (t, d, qv, r, r, qv + 1))

    def floor_():   # 無條件捨去
        d = R.randint(4, 9)
        qv, r = R.randint(3, 8), R.randint(1, d - 1)
        t = d * qv + r
        who = nm.next()
        q = "%s有 %d 元，一枝原子筆 %d 元，最多可以買幾枝？" % (who, t, d)
        return mcq(q, "%d枝" % qv, ["%d枝" % x for x in (qv + 1, r, qv - 1, d)],
                   "%d ÷ %d ＝ %d……%d，剩下的 %d 元不夠再買 1 枝，最多買 %d 枝。" % (t, d, qv, r, r, qv))
    return pick_unique(R, basic, 6, seen) + pick_unique(R, bus, 7, seen) + pick_unique(R, floor_, 7, seen)


def main():
    seen = set()
    sets = [("除法的意義：平分和每幾個一數", s1(seen)), ("九九乘法範圍的除法", fact(seen, 20)),
            ("有餘數的除法", rem(seen, 20)), ("餘數與驗算", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>平分</b>：12 顆分給 3 人，每人 4 顆，寫成 12 ÷ 3 ＝ 4。",
         "<b>每幾個一數</b>：12 顆每 3 顆裝一袋，可以裝 4 袋，也是 12 ÷ 3 ＝ 4。",
         "除法用<b>九九乘法</b>來想：3 × ？＝ 12。",
         "分不完的叫<b>餘數</b>，寫成 14 ÷ 3 ＝ 4……2。<b>餘數一定比除數小</b>。"],
        [example("29 ÷ 4 ＝", ["4 × 7 ＝ 28，4 × 8 ＝ 32 太大。", "29 － 28 ＝ 1，餘數 1 比 4 小。"], "7……1"),
         example("驗算 29 ÷ 4 ＝ 7……1", ["除數 × 商 ＋ 餘數 ＝ 被除數。", "4 × 7 ＋ 1 ＝ 29。"], "正確")],
        [("29 ÷ 4 ＝ 6……5", "餘數 5 比除數 4 大，商還可以多 1：7……1"),
         ("23 人、每頂帳篷 5 人，答 4 頂", "剩下 3 人也要睡，要 5 頂"),
         ("20 元、每枝筆 6 元，答 4 枝", "只夠買 3 枝，剩下 2 元")])
    faq = [{"q": "三年級的除法要學什麼？",
            "a": "108課綱 N-3-4：理解除法是「平分」或「每幾個一數」，用九九乘法算除法，認識餘數，並會用乘法驗算。"},
           {"q": "為什麼餘數要比除數小？",
            "a": "如果餘數和除數一樣大或更大，表示還可以再分一次，商就要再加 1。"},
           {"q": "什麼時候答案要多加 1？",
            "a": "像「至少要幾輛車、幾頂帳篷」，剩下的人也要坐，所以商要加 1；像「最多可以買幾個」，剩下的錢不夠，就不加。"}]
    make_unit(R, "grade-3", "division", "N-3-4",
              "除法：除法的意義與應用。基於N-2-9之學習，透過幾個一數的解題方法，理解如何用乘法解決除法問題。熟練十十乘法範圍的除法，做為估商的基礎。",
              "除法：平分、九九除法與餘數",
              "三年級數學 除法 練習題｜九九除法・有餘數的除法 學習單（附解答）",
              "除法與餘數",
              "國小三年級數學「除法」免費學習單：平分和包含除的意義、九九乘法範圍的除法、有餘數的除法、驗算和應用題（多一輛車、最多買幾個）。100題線上練習，附可列印解答。",
              "除法用九九想，餘數一定比除數小",
              "驗算：除數 × 商 ＋ 餘數 ＝ 被除數。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
