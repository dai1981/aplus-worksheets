# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：角與平行線（108課綱 S-8-1、S-8-3）
  python3 tools/gen_tw_math_g8_parallel_lines.py
截線で作る角の名前（對頂角・同位角・內錯角・同側內角）、平行線の截角性質で角を求める、平行の判別、式で表した角、平行線の間の點（∠APB ＝ ∠1 ＋ ∠2）。
誤答：同側內角を等しいとする（互補）、內錯角と同位角の取り違え、補角にし忘れる。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fig, svg_wrap, text, line, INK, RED, BLUE
from tw_g7 import tidy_sets

R = random.Random(81018)
POS = ["UR", "UL", "LL", "LR"]


def ang_of(theta, pos):
    return theta if pos in ("UR", "LL") else 180 - theta


def figure(theta, labels, l1="L<tspan font-size='9' dy='3'>1</tspan>", l2="L<tspan font-size='9' dy='3'>2</tspan>"):
    """labels: {(0/1, pos): 文字}。0＝上の交點、1＝下の交點"""
    W, H = 320, 220
    y1, y2 = 65, 160
    t = math.radians(max(35, min(theta, 145)))
    dx = (y2 - y1) / math.tan(t)
    xa = W / 2 + dx / 2
    xb = W / 2 - dx / 2
    s = [line(20, y1, W - 30, y1, INK, 2), line(20, y2, W - 30, y2, INK, 2),
         text(W - 22, y1 + 5, l1, 13, "start"), text(W - 22, y2 + 5, l2, 13, "start")]
    ux, uy = math.cos(t), -math.sin(t)
    s.append(line(xa + ux * 45, y1 + uy * 45, xb - ux * 45, y2 - uy * 45, BLUE, 2))
    dirs = {"R": (1, 0), "L": (-1, 0), "U": (ux, uy), "D": (-ux, -uy)}
    for (k, pos), lab in labels.items():
        cx, cy = (xa, y1) if k == 0 else (xb, y2)
        a, b = dirs[pos[1]], dirs["U" if pos[0] == "U" else "D"]
        bx, by = a[0] + b[0], a[1] + b[1]
        n = math.hypot(bx, by) or 1
        col = RED if lab in ("x", "y") or "°" not in lab else INK
        s.append(text(cx + 30 * bx / n, cy + 34 * by / n + 5, lab, 13, col=col))
    return fig(svg_wrap(W, H, "".join(s), "兩條直線被一條截線所截"))


NUM = {(0, "UL"): "1", (0, "UR"): "2", (0, "LR"): "3", (0, "LL"): "4", (1, "UL"): "5", (1, "UR"): "6", (1, "LR"): "7", (1, "LL"): "8"}


def rel(p, q):
    (k1, a), (k2, b) = p, q
    if k1 == k2:
        return "對頂角" if {a, b} in ({"UR", "LL"}, {"UL", "LR"}) else "補角（相鄰）"
    if a == b:
        return "同位角"
    top, bot = (p, q) if k1 == 0 else (q, p)
    if top[1][0] == "L" and bot[1][0] == "U":
        return "內錯角" if top[1][1] != bot[1][1] else "同側內角"
    return "其他"


def s1(seen):
    def mk():
        p, q = R.sample(list(NUM), 2)
        r = rel(p, q)
        if r in ("其他", "補角（相鄰）"):
            return None
        a, b = sorted([NUM[p], NUM[q]])
        q_ = "圖中 ∠%s 和 ∠%s 是什麼關係？" % (a, b) + figure(70, NUM)
        why = {"對頂角": "同一個交點、方向相反的兩個角是對頂角。", "同位角": "兩個交點上位置相同（同一邊、同一側）的角是同位角。",
               "內錯角": "在兩條直線之間、截線兩側交錯的角是內錯角。", "同側內角": "在兩條直線之間、截線同一側的角是同側內角。"}[r]
        return mcq(q_, r, ["對頂角", "同位角", "內錯角", "同側內角"], why)
    def partner():
        p = R.choice(list(NUM))
        kind = R.choice(["對頂角", "同位角", "內錯角", "同側內角"])
        qs = [q for q in NUM if q != p and rel(p, q) == kind]
        if not qs:
            return None
        ans = "∠" + NUM[qs[0]]
        others = ["∠" + NUM[q] for q in NUM if q != p and q != qs[0]]
        R.shuffle(others)
        q_ = "圖中 ∠%s 的%s是哪一個角？" % (NUM[p], kind) + figure(70, NUM)
        return mcq(q_, ans, others, "∠%s 和 %s 是%s。" % (NUM[p], ans, kind))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, partner, 10, seen)


def s2(seen):
    def mk():
        th = R.choice(range(40, 141, 5))
        if th == 90:
            return None
        p = (R.randint(0, 1), R.choice(POS))
        q = (1 - p[0], R.choice(POS))
        g, v = ang_of(th, p[1]), ang_of(th, q[1])
        r = rel(p, q)
        reason = {"同位角": "同位角相等", "內錯角": "內錯角相等", "同側內角": "同側內角互補"}.get(r, "利用對頂角和補角")
        q_ = "L<sub>1</sub> // L<sub>2</sub>，求 x。" + figure(th, {p: "%d°" % g, q: "x"})
        return mcq(q_, "%d°" % v, ["%d°" % w for w in (180 - v, g if g != v else v + 20, v + 10, abs(90 - v) if abs(90 - v) not in (0, v) else v - 10)],
                   "%s：x ＝ %d°。" % (reason, v) if r in ("同位角", "內錯角") else ("%s：x ＝ 180° － %d° ＝ %d°。" % (reason, g, v) if r == "同側內角" else "兩平行線的截角，銳角都相等、鈍角都相等，銳角 ＋ 鈍角 ＝ 180°：x ＝ %d°。" % v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = R.choice(range(45, 136, 5))
        if a == 90:
            continue_ = None
            return continue_
        kind = R.choice(["同位角", "內錯角", "同側內角"])
        par_ = R.random() < .5
        if kind == "同側內角":
            b = 180 - a if par_ else 180 - a + R.choice([-10, 5, 10])
            ok = a + b == 180
            cond = "%d° ＋ %d° %s 180°" % (a, b, "＝" if ok else "≠")
        else:
            b = a if par_ else a + R.choice([-10, -5, 5, 10])
            ok = a == b
            cond = "%d° %s %d°" % (a, "＝" if ok else "≠", b)
        q = "直線 L<sub>1</sub>、L<sub>2</sub> 被一條直線所截，一組%s分別是 %d° 和 %d°。L<sub>1</sub> 和 L<sub>2</sub> 平行嗎？" % (kind, a, b)
        rule = "同側內角互補" if kind == "同側內角" else "%s相等" % kind
        ans = "平行" if ok else "不平行"
        return mcq(q, ans, ["不平行" if ok else "平行", "無法判斷", "互相垂直"], "%s時兩線平行；%s，所以%s。" % (rule, cond, ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        kind = R.choice(["同位角", "內錯角", "同側內角"])
        a, c = R.randint(2, 5), R.randint(-20, 30)
        b = R.randint(1, a - 1) if a > 1 else 1
        if kind == "同側內角":
            # (a x + c) + (b x + d) = 180
            x = R.randint(10, 30)
            d = 180 - (a + b) * x - c
            if not -40 <= d <= 60 or a * x + c <= 0 or b * x + d <= 0:
                return None
            e1, e2 = "（%dx%s）°" % (a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else ""), "（%dx%s）°" % (b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "")
            q = "L<sub>1</sub> // L<sub>2</sub>，一組同側內角是%s和%s，x 是多少？" % (e1, e2)
            wrong = (d - c) // (a - b) if (d - c) % (a - b) == 0 and (d - c) // (a - b) > 0 else x + 5
            return mcq(q, str(x), [str(wrong), str(x + 2), str(180 // (a + b)) if 180 // (a + b) != x else str(x - 3)], "同側內角互補：%s ＋ %s ＝ 180°，%dx ＝ %d，x ＝ %d。" % (e1, e2, a + b, 180 - c - d, x))
        x = R.randint(10, 40)
        d = (a - b) * x + c
        if a * x + c <= 0 or a * x + c >= 180:
            return None
        e1, e2 = "（%dx%s）°" % (a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else ""), "（%sx%s）°" % ("" if b == 1 else b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "")
        q = "L<sub>1</sub> // L<sub>2</sub>，一組%s是%s和%s，x 是多少？" % (kind, e1, e2)
        wr = 180 - c - d
        return mcq(q, str(x), [str(wr // (a + b)) if wr % (a + b) == 0 and wr // (a + b) > 0 and wr // (a + b) != x else str(x + 4), str(x + 2), str(a * x + c)], "%s相等：%dx%s ＝ %sx%s，x ＝ %d（這個角是 %d°）。" % (kind, a, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else "", "" if b == 1 else b, (" ＋ %d" % d) if d > 0 else (" － %d" % -d) if d else "", x, a * x + c))
    return pick_unique(R, mk, 20, seen)


def zig(a1, a2, ask):
    W, H = 300, 180
    A, B, P = (90, 40), (90, 150), (230, 95)
    s = [line(20, 40, 280, 40, INK, 2), line(20, 150, 280, 150, INK, 2),
         text(286, 45, "L<tspan font-size='9' dy='3'>1</tspan>", 13, "start"), text(286, 155, "L<tspan font-size='9' dy='3'>2</tspan>", 13, "start"),
         line(A[0], A[1], P[0], P[1], BLUE, 2), line(B[0], B[1], P[0], P[1], BLUE, 2),
         text(A[0] - 8, A[1] - 8, "A", 13), text(B[0] - 8, B[1] + 18, "B", 13), text(P[0] + 12, P[1] + 5, "P", 13)]
    labs = {"1": a1, "2": a2, "P": ask}
    s.append(text(A[0] + 42, A[1] + 15, labs["1"], 12, col=RED if labs["1"] == "x" else INK))
    s.append(text(B[0] + 42, B[1] - 6, labs["2"], 12, col=RED if labs["2"] == "x" else INK))
    s.append(text(P[0] - 24, P[1] + 5, labs["P"], 12, col=RED if labs["P"] == "x" else INK))
    return fig(svg_wrap(W, H, "".join(s), "平行線之間的點 P"))


def s5(seen):
    def mk():
        a, b = R.randint(20, 70), R.randint(20, 70)
        k = R.choice(["P", "P", "1", "2"])
        if k == "P":
            g = zig("%d°" % a, "%d°" % b, "x")
            v, e = a + b, "過 P 畫一條和 L<sub>1</sub> 平行的線，利用內錯角相等：x ＝ %d° ＋ %d° ＝ %d°。" % (a, b, a + b)
            w = [180 - a - b, abs(a - b) if a != b else 90, 360 - a - b]
        elif k == "1":
            g = zig("x", "%d°" % b, "%d°" % (a + b))
            v, e = a, "∠APB ＝ 上方的角 ＋ 下方的角：x ＝ %d° － %d° ＝ %d°。" % (a + b, b, a)
            w = [a + 2 * b, 180 - a - b, b if b != a else a + 10]
        else:
            g = zig("%d°" % a, "x", "%d°" % (a + b))
            v, e = b, "∠APB ＝ 上方的角 ＋ 下方的角：x ＝ %d° － %d° ＝ %d°。" % (a + b, a, b)
            w = [2 * a + b, 180 - a - b, a if a != b else b + 10]
        q = "L<sub>1</sub> // L<sub>2</sub>，求 x。（圖形不一定按比例）" + g
        return mcq(q, "%d°" % v, ["%d°" % x for x in w] + ["%d°" % (v + 10)], e)
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("截線所成的角", s1(seen)), ("平行線截角求角度", s2(seen)), ("判別兩線平行", s3(seen)),
            ("列方程式求角度", s4(seen)), ("平行線之間的點", s5(seen))]
    tidy_sets(sets)
    demo = figure(70, NUM)
    body = lesson(
        ["兩條直線被一條截線所截，產生 8 個角：<b>同位角</b>（位置相同）、<b>內錯角</b>（在兩線之間、截線兩側）、<b>同側內角</b>（在兩線之間、截線同側）、<b>對頂角</b>（同一交點相對）。",
         "<b>兩線平行時</b>：同位角相等、內錯角相等、同側內角互補（和是 180°）。反過來，有這些關係就能判斷兩線平行。",
         "簡單記法：平行線被截出的角，銳角都相等、鈍角都相等，銳角 ＋ 鈍角 ＝ 180°。" + demo],
        [example("L<sub>1</sub> // L<sub>2</sub>，∠2 ＝ 70°，求 ∠8", ["∠2 和 ∠8 位置相對，∠8 ＝ ∠6（對頂角）＝ ∠2（同位角）。"], "70°"),
         example("同側內角是（2x ＋ 10）° 和（x ＋ 20）°", ["2x ＋ 10 ＋ x ＋ 20 ＝ 180。", "3x ＝ 150。"], "x ＝ 50")],
        [("同側內角相等", "同側內角互補，和是 180°"),
         ("把內錯角說成同位角", "內錯角在兩線之間，而且在截線兩側"),
         ("角度看起來一樣就說平行", "要量出或算出角的關係才能判斷")])
    faq = [{"q": "同位角、內錯角、同側內角怎麼分？",
            "a": "先看兩個角是不是在兩條直線「之間」：都在之間的，截線兩側叫內錯角、同側叫同側內角；位置一樣（同在上方右側之類）的叫同位角。"},
           {"q": "為什麼兩平行線間的點 P，∠APB ＝ ∠1 ＋ ∠2？",
            "a": "過 P 畫一條和兩線平行的直線，把 ∠APB 分成兩塊，各自和 ∠1、∠2 是內錯角，所以相等。"},
           {"q": "八年級的平行線要學什麼？",
            "a": "108課綱 S-8-1、S-8-3：對頂角、同位角、內錯角、同側內角，平行線截角性質，兩平行線間的距離處處相等。"}]
    make_unit(R, "grade-8", "parallel-lines", "S-8-3",
              "平行：平行的意義與符號；平行線截角性質；兩平行線間的距離處處相等。",
              "平行線與截角性質",
              "八年級數學 平行線 練習題｜同位角・內錯角・同側內角 學習單（附解答）",
              "平行線與截角",
              "國中八年級數學「平行線與截角性質」免費學習單：認識同位角、內錯角、同側內角和對頂角，用平行線截角求角度、判別兩線平行、列方程式求角度、平行線之間的點。100題線上練習馬上對答案，附可列印解答。",
              "同位角相等、內錯角相等、同側內角互補",
              "平行線截出的銳角都相等、鈍角都相等。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
