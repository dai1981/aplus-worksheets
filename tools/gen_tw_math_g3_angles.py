# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：角與直角（108課綱 N-3-13／S-3-1）
  python3 tools/gen_tw_math_g3_angles.py
角的頂點和邊、圖形有幾個角、直角・比直角大・比直角小、角的大小比較（邊の長さと無関係）、直角の数、時鐘的角。
三年級は「度」を使わない（度は四年級）。誤答：邊が長いほうが大きい角だと思う。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, clock, GREEN, FILL, INK, RED, BLUE

R = random.Random(31013)
NM = Names(R)


def ang_body(cx, cy, deg, l1, l2, rot, col=INK, lab=None, arc=True):
    a0 = math.radians(-rot)
    a1 = math.radians(-(rot + deg))
    x1, y1 = cx + l1 * math.cos(a0), cy + l1 * math.sin(a0)
    x2, y2 = cx + l2 * math.cos(a1), cy + l2 * math.sin(a1)
    s = [line(cx, cy, x1, y1, col, 3), line(cx, cy, x2, y2, col, 3),
         "<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx, cy, col)]
    if arc:
        r = 22
        s.append("<path d='M%.1f %.1f A%d %d 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (
            cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, cx + r * math.cos(a1), cy + r * math.sin(a1), RED))
    if lab:
        s.append(text(cx - 14, cy + 22, lab, 18, col=col))
    return "".join(s)


def one_angle(deg, rot=None):
    rot = R.choice([0, 0, 10, 20, -10]) if rot is None else rot
    l1, l2 = R.randint(90, 130), R.randint(80, 120)
    cx = 24 + max(0, -l2 * math.cos(math.radians(rot + deg)))
    return fig(svg_wrap(int(cx + l1 + 24), 170, ang_body(cx, 140, deg, l1, l2, rot), "一個角"))


def two_angles(d1, l1, d2, l2):
    c1 = 30 + max(0, -(l1 - 10) * math.cos(math.radians(d1)))
    c2 = c1 + l1 + 50 + max(0, -(l2 - 10) * math.cos(math.radians(d2)))
    s = ang_body(c1, 150, d1, l1, l1 - 10, 0, INK, "甲") + ang_body(c2, 150, d2, l2, l2 - 10, 0, INK, "乙")
    return fig(svg_wrap(int(c2 + l2 + 20), 175, s, "甲、乙兩個角"))


def poly(n, r=70, kind=None):
    pts = []
    for i in range(n):
        a = math.radians(-90 + 360 * i / n + R.choice([0, 5, -5]))
        rr = r * R.choice([1, .9, .8]) if n > 3 else r
        pts.append((90 + rr * math.cos(a), 90 + rr * math.sin(a)))
    p = " ".join("%.1f,%.1f" % xy for xy in pts)
    return fig(svg_wrap(180, 180, "<polygon points='%s' fill='%s' stroke='%s' stroke-width='3'/>" % (p, FILL, GREEN), "%d邊形" % n))


def shape_svg(kind):
    """直角の数を数える圖形"""
    w, h = R.randint(110, 170), R.randint(60, 100)
    if kind == "rect":
        pts, n, name = [(20, 20), (20 + w, 20), (20 + w, 20 + h), (20, 20 + h)], 4, "長方形"
    elif kind == "square":
        h = w = R.randint(80, 110)
        pts, n, name = [(20, 20), (20 + w, 20), (20 + w, 20 + h), (20, 20 + h)], 4, "正方形"
    elif kind == "rtri":
        pts, n, name = [(20, 20), (20, 20 + h), (20 + w, 20 + h)], 1, "三角形"
    elif kind == "rtrap":
        t = R.randint(40, w - 30)
        pts, n, name = [(20, 20), (20 + t, 20), (20 + w, 20 + h), (20, 20 + h)], 2, "梯形"
    elif kind == "para":
        o = R.randint(30, 50)
        pts, n, name = [(20 + o, 20), (20 + w, 20), (20 + w - o, 20 + h), (20, 20 + h)], 0, "平行四邊形"
    elif kind == "tri":
        pts, n, name = [(20 + w * .4, 20), (20 + w, 20 + h), (20, 20 + h)], 0, "三角形"
    else:   # L字形：6個角のうち5個が直角（1つは直角より大きい）
        a, b = R.randint(50, w - 40), R.randint(30, h - 20)
        pts, n, name = [(20, 20), (20 + a, 20), (20 + a, 20 + b), (20 + w, 20 + b), (20 + w, 20 + h), (20, 20 + h)], 5, "圖形"
    p = " ".join("%.1f,%.1f" % xy for xy in pts)
    return fig(svg_wrap(int(w + 40), int(h + 40), "<polygon points='%s' fill='%s' stroke='%s' stroke-width='3'/>" % (p, FILL, GREEN), name)), n, name


def s1(seen):
    BASICS = [("角的兩條直線叫做什麼？", "邊", ["頂點", "角", "直角"], "角是由一個頂點和兩條邊組成的。"),
              ("角的兩條邊相交的那一點叫做什麼？", "頂點", ["邊", "圓心", "直角"], "兩條邊相交的點叫做頂點。"),
              ("一個角有幾個頂點？", "1 個", ["2 個", "3 個", "4 個"], "一個角有 1 個頂點和 2 條邊。"),
              ("一個角有幾條邊？", "2 條", ["1 條", "3 條", "4 條"], "一個角有 1 個頂點和 2 條邊。"),
              ("一個長方形有幾個角？", "4 個", ["2 個", "3 個", "8 個"], "長方形有 4 條邊、4 個角。"),
              ("一個三角形有幾個角？", "3 個", ["2 個", "4 個", "6 個"], "三角形有 3 條邊、3 個角。")]
    out = [mcq(*b) for b in BASICS]
    for b in out:
        seen.add(b["q"])

    def mk():
        n = R.randint(3, 8)
        q = "這個圖形有幾個角？" + poly(n)
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (n - 1, n + 1, n * 2, n + 2)], "有 %d 個頂點，就有 %d 個角（角的數量和邊的數量一樣）。" % (n, n))
    return out + pick_unique(R, mk, 14, seen)


def s2(seen):
    def mk():
        kind = R.choice(["r", "r", "s", "b"])
        deg = 90 if kind == "r" else (R.choice([30, 40, 45, 55, 60, 70]) if kind == "s" else R.choice([115, 120, 130, 140, 150]))
        q = "這個角是直角、比直角大，還是比直角小？" + one_angle(deg)
        ans = {"r": "直角", "s": "比直角小", "b": "比直角大"}[kind]
        return mcq(q, ans, [x for x in ("直角", "比直角小", "比直角大", "要看邊多長才知道") if x != ans],
                   "用三角板的直角或摺出來的直角去比：%s。" % ("剛好疊合，是直角" if kind == "r" else ("角比直角窄，比直角小" if kind == "s" else "角比直角開，比直角大")))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        d1, d2 = R.sample([30, 45, 60, 75, 90, 110, 130, 150], 2)
        if abs(d1 - d2) < 20:
            return None
        big = "甲" if d1 > d2 else "乙"
        # 小さい角のほうの邊を長くして「邊が長い＝大きい」の誤解を確かめる
        l1, l2 = (90, 130) if big == "甲" else (130, 90)
        if R.random() < .3:
            l1 = l2 = 110
        q = "甲、乙兩個角，哪一個角比較大？" + two_angles(d1, l1, d2, l2)
        return mcq(q, big, ["乙" if big == "甲" else "甲", "一樣大", "邊比較長的角"],
                   "角的大小看兩條邊<b>張開</b>的程度，和邊的長短沒有關係。%s的角張開得比較大。" % big)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def shapes():
        kind = R.choice(["rect", "square", "rtri", "rtrap", "para", "tri", "L"])
        f, n, name = shape_svg(kind)
        q = "這個%s有幾個直角？" % name + f
        e = {"rect": "長方形的 4 個角都是直角。", "square": "正方形的 4 個角都是直角。",
             "rtri": "左下角是直角，另外 2 個角比直角小。", "rtrap": "左邊的 2 個角是直角，右邊的 2 個不是。",
             "para": "平行四邊形的角都不是直角。", "tri": "這個三角形沒有直角。",
             "L": "6 個角裡有 5 個是直角，凹進去的那個角比直角大。"}[kind]
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (4, 2, 1, 0, 6, 3) if x != n], e)

    def clock_q():
        h = R.choice([1, 2, 3, 3, 4, 5, 8, 9, 9, 10, 11])
        q = "%d 點整時，長針和短針形成的角是直角、比直角大，還是比直角小？" % h + clock(h, 0, 160)
        ans = "直角" if h in (3, 9) else ("比直角小" if h in (1, 2, 10, 11) else "比直角大")
        return mcq(q, ans, [x for x in ("直角", "比直角小", "比直角大", "沒有形成角") if x != ans],
                   "3 點和 9 點整，兩針形成直角。%d 點整%s。" % (h, "是直角" if ans == "直角" else "兩針張開得" + ("比直角小" if ans == "比直角小" else "比直角大")))
    return pick_unique(R, shapes, 12, seen) + pick_unique(R, clock_q, 8, seen)


def s5(seen):
    ITEMS = [("課本封面的角", "直角"), ("黑板的角", "直角"), ("A4 紙的角", "直角"), ("剪刀張開一點點時，兩片刀刃形成的角", "比直角小"),
             ("門打開一半時，門和牆形成的角", "比直角小"), ("躺椅往後倒，椅背和椅面形成的角", "比直角大"),
             ("把一張圓形的紙對摺兩次，摺出來的角", "直角"), ("三角板最大的角", "直角"), ("披薩切成 8 片，一片尖尖的角", "比直角小"),
             ("時鐘 9 點整，兩針形成的角", "直角"), ("時鐘 5 點整，兩針形成的角", "比直角大"), ("時鐘 1 點整，兩針形成的角", "比直角小")]
    out = []
    for it, ans in ITEMS:
        out.append(mcq("%s是直角、比直角大，還是比直角小？" % it, ans,
                       [x for x in ("直角", "比直角小", "比直角大", "沒有角") if x != ans],
                       "想一想或用三角板的直角比一比：%s%s。" % (it, "是直角" if ans == "直角" else ans)))
    for b in out:
        seen.add(b["q"])

    def cmp_word():
        a, b = NM.next(), NM.next()
        if a == b:
            return None
        da, db = R.sample([1, 2, 3, 4], 2)
        names = {1: "比直角小一點", 2: "直角", 3: "比直角大一點", 4: "比直角大很多"}
        q = "%s用兩枝筆排出的角是「%s」，%s排出的角是「%s」。誰的角比較大？" % (a, names[da], b, names[db])
        big = a if da > db else b
        return mcq(q, big, [b if big == a else a, "一樣大", "看誰的筆比較長"], "比角的大小只看張開的程度：%s的角比較大。" % big)
    return out + pick_unique(R, cmp_word, 8, seen)


def main():
    seen = set()
    sets = [("角的頂點和邊", s1(seen)), ("直角、比直角大、比直角小", s2(seen)), ("比較角的大小", s3(seen)),
            ("圖形和時鐘的直角", s4(seen)), ("生活中的角", s5(seen))]
    demo = fig(svg_wrap(220, 170, ang_body(50, 140, 90, 120, 110, 0) +
                        "<rect x='50' y='126' width='14' height='14' fill='none' stroke='%s' stroke-width='2'/>" % RED, "直角"))
    body = lesson(
        ["<b>角</b>由一個<b>頂點</b>和兩條<b>邊</b>組成。",
         "像課本封面的角、三角板最大的角，叫做<b>直角</b>。把紙對摺兩次，就能摺出直角。",
         "角的大小看兩條邊<b>張開的程度</b>，和邊畫得多長沒有關係。"],
        [example("這是直角嗎？" + demo, ["用三角板的直角對齊頂點和一條邊。", "另一條邊也剛好疊合。"], "是直角"),
         example("長方形有幾個直角？", ["長方形的 4 個角都和三角板的直角疊合。"], "4 個")],
        [("邊畫得比較長，角就比較大", "角的大小只看張開的程度"),
         ("圖形斜放就不是直角", "轉個方向，直角還是直角"),
         ("平行四邊形也有 4 個直角", "要用三角板量一量，平行四邊形的角不是直角")])
    faq = [{"q": "三年級的角要學到幾度嗎？",
            "a": "不用。108課綱 N-3-13／S-3-1 在三年級只要認識角、比較角的大小和認識直角；用量角器量「度」是四年級的內容。"},
           {"q": "怎麼比較兩個角的大小？",
            "a": "直接比較：把兩個角的頂點和一條邊疊在一起，看另一條邊。間接比較：用描圖紙或三角板的直角當作中間的工具。"},
           {"q": "孩子以為邊長的角比較大，怎麼教？",
            "a": "用兩枝長短不同的吸管做角，張開一樣多時，角一樣大；讓孩子看到角的大小只和張開的程度有關。"}]
    make_unit(R, "grade-3", "angles", "S-3-1",
              "角與角度（同 N-3-13）：以具體操作為主。初步認識角和角度。角度的直接比較與間接比較。認識直角。",
              "角與直角：頂點、邊、比較角的大小",
              "三年級數學 角與直角 練習題｜認識角・直角・比較角的大小 學習單（附解答）",
              "角與直角",
              "國小三年級數學「角與直角」免費學習單：認識角的頂點和邊、直角、比直角大或小、比較角的大小、圖形和時鐘的直角。100題線上練習馬上對答案，附可列印解答。",
              "角的大小看張開的程度",
              "像課本封面的角是直角；邊的長短和角的大小無關。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
