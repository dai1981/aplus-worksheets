# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：幾何符號與垂直（108課綱 S-7-1、S-7-3）
  python3 tools/gen_tw_math_g7_geometry_symbols_and_perpendicular.py
點・直線・線段・射線の記號（AB 上に – ↔ →）、角（∠ABC：頂點は真ん中）、三角形（△ABC）、垂直（⊥）、中垂線（線段を垂直に二等分・中垂線上の點は兩端點から等距離）、點到直線距離（垂線段の長さ）。
誤答：射線の端點を逆にする、∠ABC の頂點を A とする、斜めの線分を距離とする、中垂線上の點までの距離を片方だけ伸ばす。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, INK, RED, BLUE
from tw_g7 import tidy_sets

R = random.Random(71022)
NM = Names(R)
L = "ABCDEFGHPQ"


def ov(a, b, kind):
    """記號：線段 AB（上に ─）、直線 AB（↔）、射線 AB（→）"""
    mark = {"seg": "‾", "line": "↔", "ray": "→"}[kind]
    return "<span style='white-space:nowrap'>%s%s</span>" % (a + b, "<sup>" + mark + "</sup>")


def s1(seen):
    def mk():
        a, b = R.sample(L[:8], 2)
        kind = R.choice(["seg", "line", "ray"])
        desc = {"seg": "有兩個端點 %s、%s，長度固定" % (a, b), "line": "通過 %s、%s，向兩邊無限延伸" % (a, b), "ray": "從端點 %s 出發，經過 %s 一直延伸" % (a, b)}[kind]
        name = {"seg": "線段 " + a + b, "line": "直線 " + a + b, "ray": "射線 " + a + b}[kind]
        others = [n for n in ("線段 " + a + b, "直線 " + a + b, "射線 " + a + b, "射線 " + b + a) if n != name]
        return mcq("「%s」的圖形叫做什麼？" % desc, name, others, "線段有兩個端點；直線沒有端點；射線只有一個端點，寫在前面。")
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def ang():
        a, b, c = R.sample(L[:8], 3)
        q = "∠%s%s%s 的頂點是哪一點？" % (a, b, c)
        return mcq(q, b, [a, c, "沒有頂點"], "用三個字母表示角時，中間的字母是頂點：∠%s%s%s 的頂點是 %s。" % (a, b, c, b))

    def same():
        a, b, c = R.sample(L[:8], 3)
        q = "下面哪一個和 ∠%s%s%s 表示同一個角？" % (a, b, c)
        return mcq(q, "∠%s%s%s" % (c, b, a), ["∠%s%s%s" % (b, a, c), "∠%s%s%s" % (a, c, b), "∠%s%s%s" % (b, c, a)], "頂點 %s 要在中間，兩邊的字母可以對調。" % b)

    def tri():
        F_ = [("「△ABC」表示什麼？", "以 A、B、C 為頂點的三角形", ["∠ABC", "線段 ABC", "A、B、C 三點在同一直線上"], "△ 是三角形的符號。"),
              ("「AB ⊥ CD」表示什麼？", "AB 和 CD 互相垂直", ["AB 和 CD 平行", "AB 和 CD 一樣長", "AB 是 CD 的一半"], "⊥ 是垂直的符號。"),
              ("「AB ∥ CD」表示什麼？", "AB 和 CD 互相平行", ["AB 和 CD 垂直", "AB 和 CD 相交", "AB 比 CD 長"], "∥ 是平行的符號。"),
              ("兩條直線互相垂直，相交成的角是幾度？", "90 度", ["45 度", "180 度", "60 度"], "垂直就是相交成直角。"),
              ("「AB ＝ CD」表示什麼？", "線段 AB 和線段 CD 一樣長", ["AB 和 CD 是同一條線段", "AB 和 CD 平行", "AB ⊥ CD"], "等號表示兩線段長度相等。"),
              ("經過兩點可以畫幾條直線？", "1 條", ["2 條", "無限多條", "0 條"], "兩點決定一條直線。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, ang, 8, seen) + pick_unique(R, same, 6, seen) + pick_unique(R, tri, 6, seen)


def perp_svg(d, slants):
    """直線 L と點 P、垂線段（長さ d）と斜めの線段"""
    W, H = 300, 170
    s = [line(20, 140, 280, 140, INK, 2), text(286, 144, "L", 13, anchor="start")]
    px = 150
    py = 140 - d * 10
    s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (px, py, RED))
    s.append(text(px, py - 8, "P", 13, col=RED))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='140' stroke='%s' stroke-width='2.2'/>" % (px, py, px, BLUE))
    s.append("<path d='M%d 140 v-10 h10' fill='none' stroke='%s' stroke-width='1.4'/>" % (px, INK))
    s.append(text(px - 8, 158, "H", 12))
    s.append(text(px + 6, (py + 140) / 2 + 4, "%d" % d, 12, anchor="start", col=BLUE))
    for i, (off, ln) in enumerate(slants):
        x = px + off
        s.append("<line x1='%d' y1='%d' x2='%d' y2='140' stroke='#888' stroke-width='1.6' stroke-dasharray='5 3'/>" % (px, py, x))
        s.append(text(x, 158, "QR"[i], 12))
        s.append(text((px + x) / 2 + (8 if off > 0 else -8), (py + 140) / 2 - 4, "%d" % ln, 12, anchor="start" if off > 0 else "end", col="#666"))
    return fig(svg_wrap(W, H, "".join(s), "點 P 到直線 L 的距離"))


def s3(seen):
    def mk():
        d = R.randint(3, 9)
        l1, l2 = d + R.randint(1, 5), d + R.randint(1, 6)
        if l1 == l2:
            return None
        off = lambda l: int(round(((l * l - d * d) ** .5) * 10))
        g = perp_svg(d, [(off(l1), l1), (-off(l2), l2)])
        return mcq("PH ⊥ L。點 P 到直線 L 的距離是多少？" + g, str(d), [str(l1), str(l2), str(l1 + l2)], "點到直線的距離是<b>垂線段</b> PH 的長度 %d，也是所有連線中最短的。" % d)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        d = R.randint(3, 20)
        k = R.choice(["pa", "half", "angle"])
        if k == "pa":
            q = "直線 M 是線段 AB 的中垂線，P 在 M 上，PA ＝ %d。PB ＝ ？" % d
            return mcq(q, str(d), [str(d * 2), str(d // 2) if d > 3 else str(d + 2), "無法知道"], "中垂線上任一點到線段兩端點的距離相等：PB ＝ PA ＝ %d。" % d)
        if k == "half":
            q = "直線 M 是線段 AB 的中垂線，交 AB 於 O。AB ＝ %d，AO ＝ ？" % (2 * d)
            return mcq(q, str(d), [str(2 * d), str(d + 1), str(4 * d)], "中垂線把線段平分：AO ＝ %d ÷ 2 ＝ %d。" % (2 * d, d))
        q = "直線 M 是線段 AB 的中垂線，交 AB 於 O。M 和 AB 的夾角是幾度？"
        return mcq(q, "90 度", ["45 度", "180 度", "60 度"], "中垂線和線段垂直，夾角 90 度。")

    def tri():
        a, b = R.randint(5, 15), R.randint(4, 12)
        q = "P 在線段 AB 的中垂線上，PA ＝ %d，AB ＝ %d。△PAB 的周長是多少？" % (a, b)
        return mcq(q, str(2 * a + b), [str(a + b), str(2 * a + 2 * b), str(a * 2)], "PB ＝ PA ＝ %d，周長 ＝ %d ＋ %d ＋ %d ＝ %d。" % (a, a, a, b, 2 * a + b))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, tri, 10, seen)


def s5(seen):
    def mk():
        F_ = [("直線 L 外一點 P，連到 L 上各點的線段中，最短的是哪一條？", "垂直於 L 的垂線段", ["和 L 平行的線段", "最斜的線段", "每一條都一樣長"], "垂線段最短，它的長度就是點到直線的距離。"),
              ("線段的中垂線有什麼特徵？", "通過線段中點，而且和線段垂直", ["只通過線段中點", "只和線段垂直", "和線段平行"], "中垂線 ＝ 中點 ＋ 垂直。"),
              ("到線段 AB 兩端點距離相等的點，都在哪裡？", "AB 的中垂線上", ["AB 上", "以 A 為圓心的圓上", "AB 的延長線上"], "中垂線上的點到兩端等距，反過來也成立。"),
              ("射線 AB 和射線 BA 是同一條射線嗎？", "不是，端點不同", ["是，字母一樣", "是，方向相同", "不一定"], "射線的端點寫在前面：AB 的端點是 A，BA 的端點是 B。"),
              ("線段 AB 和線段 BA 是同一條線段嗎？", "是", ["不是，方向不同", "不一定", "只有長度一樣"], "線段沒有方向，AB 和 BA 是同一條。"),
              ("直線可以量出長度嗎？", "不可以，直線無限延伸", ["可以，用尺量", "只能量一半", "要看畫多長"], "直線和射線都無限延伸，沒有長度；線段才有長度。"),
              ("平面上，過直線外一點可以畫幾條和這條直線垂直的直線？", "1 條", ["2 條", "無限多條", "0 條"], "過直線外一點只能畫一條垂線。"),
              ("點 P 到直線 L 的距離是 0，表示什麼？", "P 在 L 上", ["P 離 L 很遠", "P 在 L 的垂線上", "無法判斷"], "距離是 0，點就在直線上。")]
        return mcq(*R.choice(F_))
    out = pick_unique(R, mk, 8, seen)

    def town():
        d1 = R.randint(3, 12)
        q = "A、B 兩村要在一條直路 L 上蓋一個公車站 P，使 PA ＝ PB。P 應該蓋在哪裡？"
        return mcq(q, "AB 的中垂線和 L 的交點", ["A 到 L 的垂足", "AB 的中點", "B 到 L 的垂足"], "到 A、B 等距的點在 AB 的中垂線上，又要在路 L 上，所以取交點。")

    def well():
        d = R.randint(50, 400)
        q = "小鎮 P 到一條直線河 L 的距離是 %d 公尺。從 P 開一條水管到河邊，最短要幾公尺？" % d
        return mcq(q, "%d 公尺" % d, ["%d 公尺" % (d * 2), "%d 公尺" % (d + 50), "無法知道"], "最短的是垂線段，長度就是點到直線的距離 %d 公尺。" % d)
    return out + pick_unique(R, town, 1, seen) + pick_unique(R, well, 11, seen)


def main():
    seen = set()
    sets = [("直線、線段、射線", s1(seen)), ("角和符號", s2(seen)), ("點到直線的距離", s3(seen)),
            ("中垂線", s4(seen)), ("觀念與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>線段 AB</b> 有兩個端點；<b>直線 AB</b> 兩邊無限延伸；<b>射線 AB</b> 從端點 A 出發經過 B 延伸。",
         "<b>∠ABC</b> 的頂點是中間的 B；△ABC 是三角形；AB ⊥ CD 表示垂直，AB ∥ CD 表示平行。",
         "點到直線的<b>距離</b>是垂線段的長度，也是最短的連線。",
         "<b>中垂線</b>：通過線段中點且垂直的直線。中垂線上的點到線段兩端<b>等距</b>。"],
        [example("∠PQR 的頂點是？", ["中間的字母。"], "Q"),
         example("P 在 AB 的中垂線上，PA ＝ 7，PB ＝ ？", ["中垂線上的點到兩端等距。"], "7")],
        [("∠ABC 的頂點是 A", "頂點是中間的 B"),
         ("射線 AB 和射線 BA 一樣", "端點不同，方向相反"),
         ("點到直線的距離用斜的線段量", "要用垂線段")])
    faq = [{"q": "線段、直線、射線怎麼分辨？",
            "a": "看端點：線段有兩個端點、可以量長度；射線有一個端點、向一邊無限延伸；直線沒有端點、向兩邊無限延伸。"},
           {"q": "中垂線有什麼用？",
            "a": "中垂線上的每一點到線段兩端點的距離都相等，可以用來找「到兩地一樣遠」的位置。"},
           {"q": "七年級的幾何符號要學什麼？",
            "a": "108課綱 S-7-1、S-7-3：點、線、線段、射線、角、三角形與其符號，垂直的符號、線段的中垂線、點到直線距離的意義。"}]
    make_unit(R, "grade-7", "geometry-symbols-and-perpendicular", "S-7-3",
              "垂直：垂直的符號；線段的中垂線；點到直線距離的意義。",
              "幾何符號、垂直與中垂線",
              "七年級數學 幾何符號 練習題｜線段・射線・∠・⊥・中垂線 學習單（附解答）",
              "幾何符號與垂直",
              "國中七年級數學「幾何符號、垂直與中垂線」免費學習單：直線、線段、射線的區別，角和三角形的符號，點到直線的距離，中垂線的性質與應用。100題線上練習馬上對答案，附可列印解答。",
              "點到直線的距離是垂線段的長",
              "中垂線上的點到線段兩端等距。",
              body, faq, sets, 22)


if __name__ == "__main__":
    main()
