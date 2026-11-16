# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：相似形（108課綱 S-9-1）
  python3 tools/gen_tw_math_g9_similar_figures.py
縮放と相似、相似かどうか（長方形・正方形・菱形など）、對應角相等・對應邊成比例、相似比から邊・周長、縮放の倍率。
誤答：邊の差が同じなら相似とする、對應邊を取り違える、相似比を逆にする、角も倍にする。
"""
import random
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, num, fr
from tw_g7 import tidy_sets
from tw_g9 import ov, poly_svg

R = random.Random(81102)


def ratio(a, b):
    g = gcd(a, b)
    return "%d：%d" % (a // g, b // g)


def s1(seen):
    FACTS = [("任意兩個正方形一定相似嗎？", "一定相似", "四個角都是 90°，四邊的比也都相等，所以一定相似。"),
             ("任意兩個長方形一定相似嗎？", "不一定相似", "角都相等，但長和寬的比不一定相同，例如 1 × 2 和 1 × 3。"),
             ("任意兩個菱形一定相似嗎？", "不一定相似", "邊的比相同，但角不一定相等。"),
             ("任意兩個正三角形一定相似嗎？", "一定相似", "三個角都是 60°，三邊的比也相等。"),
             ("任意兩個圓一定相似嗎？", "一定相似", "所有的圓形狀都一樣，只有大小不同。"),
             ("任意兩個等腰三角形一定相似嗎？", "不一定相似", "頂角不同時形狀就不同。"),
             ("任意兩個正五邊形一定相似嗎？", "一定相似", "每個內角都是 108°，邊的比也相等。"),
             ("全等的兩個圖形一定相似嗎？", "一定相似", "全等是相似比 1：1 的相似。")]
    out = [mcq(q, a, ["不一定相似" if a == "一定相似" else "一定相似", "一定不相似", "只有面積相同才相似"], e) for q, a, e in FACTS]
    for b in out:
        seen.add(b["q"])

    def rect():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a == b:
            return None
        k = R.choice([2, 3, 4])
        ok = R.random() < .5
        c, d = (a * k, b * k) if ok else (a + k, b + k)
        q = "長 %d、寬 %d 的長方形，和長 %d、寬 %d 的長方形相似嗎？" % (max(a, b), min(a, b), max(c, d), min(c, d))
        ans = "相似" if ok else "不相似"
        return mcq(q, ans, ["不相似" if ok else "相似", "要看面積", "無法判斷"], ("長和寬都放大 %d 倍，對應邊成比例，所以相似。" % k) if ok else "長寬都加 %d，比 %s 和 %s 不相等，所以不相似。" % (k, ratio(max(a, b), min(a, b)), ratio(max(c, d), min(c, d))))
    return out + pick_unique(R, rect, 12, seen)


def s2(seen):
    def mk():
        a, b = R.randint(3, 12), R.randint(3, 12)
        if a == b:
            return None
        k = R.choice([2, 3, 4, 5])
        h = R.choice([1, 2])
        A, B = a * k, b * k
        if h == 2 and (A % 2 or B % 2):
            return None
        pts1 = {"A": (0, 0), "B": (a * 14, 0), "C": (a * 14, b * 14), "D": (0, b * 14)}
        q = "長方形 ABCD ～ 長方形 PQRS，%s ＝ %d，%s ＝ %d，%s ＝ %d，%s 是多少？" % (ov("AB"), a, ov("BC"), b, ov("PQ"), A, ov("QR"))
        return mcq(q, str(B), [str(b + A - a), str(A * a // b) if A * a % b == 0 and A * a // b != B else str(B + k), str(b * a)], "相似比 ＝ %s：%s ＝ %d：%d ＝ 1：%d，%s ＝ %d × %d ＝ %d。" % (ov("AB"), ov("PQ"), a, A, k, ov("QR"), b, k, B))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def ang():
        a, b, c = R.randint(60, 130), R.randint(60, 120), R.randint(60, 120)
        d = 360 - a - b - c
        if not 40 <= d <= 150:
            return None
        k = R.choice(["P", "Q", "R", "S"])
        v = {"P": a, "Q": b, "R": c, "S": d}[k]
        q = "四邊形 ABCD ～ 四邊形 PQRS，∠A ＝ %d°，∠B ＝ %d°，∠C ＝ %d°，∠%s 是多少度？" % (a, b, c, k)
        return mcq(q, "%d°" % v, ["%d°" % x for x in {a, b, c, d, 2 * v if 2 * v < 360 else v // 2} if x != v], "相似形的對應角相等：∠%s ＝ ∠%s%s。" % (k, "ABCD"["PQRS".index(k)], "" if k != "S" else "，∠D ＝ 360° － %d° － %d° － %d° ＝ %d°" % (a, b, c, d)))

    def tri():
        A, B, C = R.sample(range(3, 15), 3)
        if max(A, B, C) * 2 >= A + B + C:
            return None
        k = R.choice([2, 3])
        q = "△ABC ～ △DEF，%s ＝ %d，%s ＝ %d，%s ＝ %d，%s ＝ %d，%s 是多少？" % (ov("AB"), A, ov("BC"), B, ov("CA"), C, ov("DE"), A * k, ov("FD"))
        v = C * k
        return mcq(q, str(v), [str(B * k), str(C + A * k - A), str(A * k)], "相似比 %d：%d ＝ 1：%d，%s 對應 %s：%d × %d ＝ %d。" % (A, A * k, k, ov("FD"), ov("CA"), C, k, v))
    return pick_unique(R, ang, 10, seen) + pick_unique(R, tri, 10, seen)


def s4(seen):
    def peri():
        a, b = R.randint(1, 6), R.randint(1, 6)
        if a == b or gcd(a, b) > 1:
            return None
        P = R.randint(3, 15) * a
        q = "兩個相似多邊形的相似比是 %d：%d，小的周長是 %d 公分，大的周長是多少公分？" % (min(a, b), max(a, b), P if a < b else P)
        lo, hi = min(a, b), max(a, b)
        if P % lo:
            return None
        v = P // lo * hi
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (P // lo * hi * hi // lo if P * hi * hi % (lo * lo) == 0 and P * hi * hi // (lo * lo) != v else v + hi, P + hi - lo, P * lo // hi if P * lo % hi == 0 else v - lo)], "周長的比 ＝ 相似比 ＝ %d：%d，%d ÷ %d × %d ＝ %d。" % (lo, hi, P, lo, hi, v))

    def scale():
        a = R.randint(2, 12)
        k = R.choice([2, 3, 4, 5])
        down = R.random() < .4
        if down:
            q = "把邊長 %d 公分的正方形縮小成 <span class='fr'><span class='fn'>1</span><span class='fd'>%d</span></span> 倍，新正方形每個角是幾度、邊長多少？" % (a * k, k)
            return mcq(q, "90°，%d 公分" % a, ["%s°，%d 公分" % (fr(90, k) if 90 % k else 90 // k, a), "90°，%d 公分" % (a * k - k), "45°，%d 公分" % a], "縮放時角度不變，邊長都乘以 1/%d：%d ÷ %d ＝ %d。" % (k, a * k, k, a))
        q = "把一個三角形放大成 %d 倍，有一個角是 40°，放大後這個角是幾度？" % k
        return mcq(q, "40°", ["%d°" % (40 * k), "%d°" % (40 + k), "%d°" % (180 - 40 * k) if 180 - 40 * k > 0 else "20°"], "放大或縮小，角度都不變，只有邊長改變。")
    return pick_unique(R, peri, 14, seen) + pick_unique(R, scale, 6, seen)


def s5(seen):
    def photo():
        w, h = R.choice([(4, 6), (3, 5), (5, 7), (6, 8), (8, 10)])
        k = R.choice([2, 3, 4, 5])
        q = "一張 %d 公分 × %d 公分的照片，放大成相似的照片，短邊變成 %d 公分，長邊是多少公分？" % (w, h, w * k)
        v = h * k
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (h + w * k - w, h * w * k // w if False else h * k + k, w * k * k)], "相似比 %d：%d ＝ 1：%d，長邊 %d × %d ＝ %d 公分。" % (w, w * k, k, h, k, v))

    def mapq():
        s_ = R.choice([1000, 2000, 5000, 10000, 25000])
        cm = R.randint(2, 15)
        real = cm * s_ // 100
        q = "比例尺 1：%s 的地圖上，兩地相距 %d 公分，實際距離是多少公尺？" % (num(s_), cm)
        return mcq(q, "%s 公尺" % num(real), ["%s 公尺" % num(x) for x in (cm * s_, real // 10 if real >= 10 else real * 100, real * 10)], "地圖和實際是相似形：%d × %s ＝ %s 公分 ＝ %s 公尺。" % (cm, num(s_), num(cm * s_), num(real)))

    def model():
        r = R.choice([10, 20, 25, 50, 100])
        L = R.choice([2, 3, 4, 5, 6, 8]) * r
        q = "一個 1：%d 的建築模型，模型高 %d 公分，真實建築高多少公尺？" % (r, L // r)
        v = L // 100 if L % 100 == 0 else None
        if v is None:
            return None
        return mcq(q, "%d 公尺" % v, ["%d 公尺" % x for x in (L, L // 10 if L // 10 != v else v + 1, v * 10)], "%d × %d ＝ %d 公分 ＝ %d 公尺。" % (L // r, r, L, v))
    return pick_unique(R, photo, 7, seen) + pick_unique(R, mapq, 7, seen) + pick_unique(R, model, 6, seen)


def main():
    seen = set()
    sets = [("認識相似", s1(seen)), ("相似比求邊長", s2(seen)), ("對應角與對應邊", s3(seen)),
            ("周長的比與縮放", s4(seen)), ("生活中的相似", s5(seen))]
    tidy_sets(sets)
    demo = poly_svg({"A": (0, 0), "B": (60, 0), "C": (60, 40), "D": (0, 40)}, [["A", "B", "C", "D", "A"]], {("A", "B"): "3", ("B", "C"): "2"}, label="長方形 ABCD")
    demo2 = poly_svg({"P": (0, 0), "Q": (120, 0), "R": (120, 80), "S": (0, 80)}, [["P", "Q", "R", "S", "P"]], {("P", "Q"): "6", ("Q", "R"): "4"}, label="長方形 PQRS")
    body = lesson(
        ["一個圖形放大或縮小後得到的圖形和原圖形<b>相似</b>，記成「～」，例如 ABCD ～ PQRS（頂點按對應順序寫）。",
         "多邊形相似：<b>對應角相等，而且對應邊成比例</b>。對應邊的比叫<b>相似比</b>。",
         "相似形的周長比 ＝ 相似比；放大縮小時角度不變。" + demo + demo2],
        [example("ABCD ～ PQRS，AB ＝ 3，PQ ＝ 6，BC ＝ 2，QR？", ["相似比 3：6 ＝ 1：2。", "QR ＝ 2 × 2。"], "4"),
         example("長 6 寬 4 和長 9 寬 6 的長方形相似嗎？", ["6：4 ＝ 3：2，9：6 ＝ 3：2。"], "相似")],
        [("長、寬都加 2 也相似", "要都乘以同一個數，比才不變"),
         ("放大 2 倍，角也變 2 倍", "角度不變"),
         ("所有長方形都相似", "長寬比不同就不相似")])
    faq = [{"q": "相似和全等有什麼不同？",
            "a": "全等是形狀和大小都一樣；相似只要形狀一樣，大小可以不同。全等是相似比 1：1 的特別情形。"},
           {"q": "怎麼判斷兩個多邊形相似？",
            "a": "要同時符合兩個條件：對應角都相等、對應邊都成比例。只有一個條件不夠，例如長方形和正方形角都相等卻不相似。"},
           {"q": "九年級的相似形要學什麼？",
            "a": "108課綱 S-9-1：平面圖形縮放的意義，多邊形相似的意義，對應角相等、對應邊長成比例。"}]
    make_unit(R, "grade-9", "similar-figures", "S-9-1",
              "相似形：平面圖形縮放的意義；多邊形相似的意義；對應角相等；對應邊長成比例。",
              "相似形：對應角與對應邊",
              "九年級數學 相似形 練習題｜相似比・對應邊成比例 學習單（附解答）",
              "相似形",
              "國中九年級數學「相似形」免費學習單：認識相似、用相似比求邊長、對應角相等與對應邊成比例、周長比與縮放、照片放大和地圖比例尺。100題線上練習馬上對答案，附可列印解答。",
              "對應角相等，對應邊成比例",
              "相似形的周長比 ＝ 相似比；縮放時角度不變。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
