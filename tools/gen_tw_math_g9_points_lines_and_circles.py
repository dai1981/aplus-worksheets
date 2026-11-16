# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：點、直線與圓的關係（108課綱 S-9-7、S-9-6 切線段等長）
  python3 tools/gen_tw_math_g9_points_lines_and_circles.py
點と圓（d と r の比較）、直線と圓（不相交・相切・兩交點）、切線は半徑に垂直（畢氏定理で切線段）、弦心距は弦を垂直平分、外部の點からの二本の切線段は等長、兩圓の位置。
誤答：弦の長さを半分にしない、切線段で r² ＋ d² にする、d ＝ r を內部とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets
from tw_g9 import ov

R = random.Random(81107)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26), (20, 21, 29), (12, 35, 37), (9, 40, 41)]


def s1(seen):
    def pt():
        r = R.randint(3, 20)
        d = R.choice([r - R.randint(1, r - 1), r, r + R.randint(1, 10)])
        ans = "圓內部" if d < r else "圓上" if d == r else "圓外部"
        q = "圓 O 的半徑是 %d，點 P 到圓心的距離 %s ＝ %d，P 在哪裡？" % (r, ov("OP"), d)
        return mcq(q, ans, ["圓內部", "圓上", "圓外部", "圓心"], "比較距離和半徑：%d %s %d，所以 P 在%s。" % (d, "＜" if d < r else "＝" if d == r else "＞", r, ans))

    def ln():
        r = R.randint(3, 20)
        d = R.choice([r - R.randint(1, r - 1), r, r + R.randint(1, 10)])
        ans = "交於兩點" if d < r else "相切（交於一點）" if d == r else "不相交"
        q = "圓 O 的半徑是 %d，圓心到直線 L 的距離是 %d，L 和圓 O 的關係是？" % (r, d)
        return mcq(q, ans, ["交於兩點", "相切（交於一點）", "不相交", "交於三點"], "圓心到直線的距離 %d %s 半徑 %d，所以%s。" % (d, "＜" if d < r else "＝" if d == r else "＞", r, ans))
    return pick_unique(R, pt, 10, seen) + pick_unique(R, ln, 10, seen)


def s2(seen):
    def mk():
        a, b, c = R.choice(TRIP)
        a, b = R.sample([a, b], 2)
        t = R.choice(["PA", "OP", "r"])
        if t == "PA":
            q = "%s 切圓 O 於 A，半徑 %s ＝ %d，%s ＝ %d，切線段 %s 是多少？" % (ov("PA"), ov("OA"), a, ov("OP"), c, ov("PA"))
            v, w = b, [c - a, c + a, a]
            e = "切線垂直於過切點的半徑，∠OAP ＝ 90°：%s ＝ √（%d<sup>2</sup> － %d<sup>2</sup>）＝ %d。" % (ov("PA"), c, a, b)
        elif t == "OP":
            q = "%s 切圓 O 於 A，半徑 %s ＝ %d，切線段 %s ＝ %d，%s 是多少？" % (ov("PA"), ov("OA"), a, ov("PA"), b, ov("OP"))
            v, w = c, [a + b, abs(b - a) if abs(b - a) != c else c + 1, c + 2]
            e = "∠OAP ＝ 90°：%s ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d。" % (ov("OP"), a, b, c)
        else:
            q = "%s 切圓 O 於 A，%s ＝ %d，%s ＝ %d，圓 O 的半徑是多少？" % (ov("PA"), ov("PA"), b, ov("OP"), c)
            v, w = a, [c - b if c - b != a else a + 1, c + b, b]
            e = "∠OAP ＝ 90°：半徑 ＝ √（%d<sup>2</sup> － %d<sup>2</sup>）＝ %d。" % (c, b, a)
        return mcq(q, str(v), [str(x) for x in w if x != v] + [str(v + 3)], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b, c = R.choice(TRIP)
        d, h = R.sample([a, b], 2)
        t = R.choice(["chord", "d", "r"])
        if t == "chord":
            q = "圓 O 的半徑是 %d，弦 %s 到圓心的距離（弦心距）是 %d，%s 長多少？" % (c, ov("AB"), d, ov("AB"))
            v, w = 2 * h, [h, 2 * c, c - d]
            e = "弦心距垂直平分弦：半弦 ＝ √（%d<sup>2</sup> － %d<sup>2</sup>）＝ %d，%s ＝ 2 × %d ＝ %d。" % (c, d, h, ov("AB"), h, 2 * h)
        elif t == "d":
            q = "圓 O 的半徑是 %d，弦 %s 長 %d，弦心距是多少？" % (c, ov("AB"), 2 * h)
            v, w = d, [c - h if c - h != d else d + 1, 2 * d, h]
            e = "半弦 %d，弦心距 ＝ √（%d<sup>2</sup> － %d<sup>2</sup>）＝ %d。" % (h, c, h, d)
        else:
            q = "圓 O 中，弦 %s 長 %d，弦心距是 %d，半徑是多少？" % (ov("AB"), 2 * h, d)
            v, w = c, [h + d, 2 * c, c + 1]
            e = "半徑 ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d（半弦是 %d）。" % (h, d, c, h)
        return mcq(q, str(v), [str(x) for x in w if x != v] + [str(v + 2)], e)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def tan2():
        a = R.randint(3, 20)
        q = "從圓外一點 P 畫兩條切線，切點分別是 A、B，%s ＝ %d，%s 是多少？" % (ov("PA"), a, ov("PB"))
        return mcq(q, str(a), [str(2 * a), str(a // 2) if a % 2 == 0 else str(a + 1), str(a * a)], "從圓外一點到圓的兩條切線段等長：%s ＝ %s ＝ %d。" % (ov("PB"), ov("PA"), a))

    def angle():
        p = R.randint(30, 140)
        q = "從圓外一點 P 畫兩條切線，切點是 A、B，∠APB ＝ %d°，∠AOB 是多少度（O 是圓心）？" % p
        return mcq(q, "%d°" % (180 - p), ["%d°" % x for x in (p, 360 - p, 90 - p // 2 if 90 - p // 2 != 180 - p else 180 - p + 10)], "∠OAP ＝ ∠OBP ＝ 90°，四邊形內角和 360°：∠AOB ＝ 360° － 90° － 90° － %d° ＝ %d°。" % (p, 180 - p))

    def tri_in():
        x, y, z = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
        q = "圓和 △ABC 的三邊都相切，從 A、B、C 到切點的切線段長分別是 %d、%d、%d，△ABC 的周長是多少？" % (x, y, z)
        return mcq(q, str(2 * (x + y + z)), [str(x + y + z), str(3 * (x + y + z)), str(2 * (x + y + z) - 1)], "每個頂點的兩條切線段等長，每邊由兩段組成：周長 ＝ 2 ×（%d ＋ %d ＋ %d）＝ %d。" % (x, y, z, 2 * (x + y + z)))
    return pick_unique(R, tan2, 7, seen) + pick_unique(R, angle, 7, seen) + pick_unique(R, tri_in, 6, seen)


def s5(seen):
    def arch():
        a, b, c = R.choice(TRIP)
        d, h = R.sample([a, b], 2)
        if c - d <= 0:
            return None
        q = "一座圓弧形拱橋，橋下水面寬（弦長）%d 公尺，拱頂離水面高 %d 公尺。這個圓弧的半徑是多少公尺？" % (2 * h, c - d)
        return mcq(q, "%d 公尺" % c, ["%d 公尺" % x for x in (h, d, h + c - d, c + 1)], "設半徑 r，弦心距 r － %d，半弦 %d：（r － %d）<sup>2</sup> ＋ %d<sup>2</sup> ＝ r<sup>2</sup>，r ＝ %d。" % (c - d, h, c - d, h, c))

    def wheel():
        a, b, c = R.choice(TRIP[:8])
        q = "一個半徑 %d 公分的輪子放在地上，地面是輪子的切線。地面上一點 P 和切點相距 %d 公分，P 到輪軸（圓心）的距離是多少公分？" % (a, b)
        return mcq(q, "%d 公分" % c, ["%d 公分" % x for x in (a + b, b, c + 1)], "半徑垂直地面：√（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d。" % (a, b, c))
    return pick_unique(R, arch, 12, seen) + pick_unique(R, wheel, 8, seen)


def main():
    seen = set()
    sets = [("點、直線和圓的位置", s1(seen)), ("切線垂直半徑", s2(seen)), ("弦心距", s3(seen)),
            ("切線段等長", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["點 P 到圓心的距離 d 和半徑 r 比：d ＜ r 在圓內，d ＝ r 在圓上，d ＞ r 在圓外。直線也一樣：圓心到直線的距離 ＜ r 交於兩點、＝ r 相切、＞ r 不相交。",
         "<b>切線垂直於過切點的半徑</b>，常和畢氏定理一起用。",
         "<b>弦心距垂直平分弦</b>：半弦<sup>2</sup> ＋ 弦心距<sup>2</sup> ＝ 半徑<sup>2</sup>。",
         "<b>從圓外一點畫兩條切線，兩條切線段等長</b>。"],
        [example("半徑 5，弦心距 3，弦長？", ["半弦 √（25 － 9）＝ 4。", "弦長 2 × 4。"], "8"),
         example("切線段 PA，OA ＝ 6，OP ＝ 10，PA？", ["∠OAP ＝ 90°，PA ＝ √（100 － 36）。"], "8")],
        [("弦長就是 √（r<sup>2</sup> － d<sup>2</sup>）", "那是半弦，要 × 2"),
         ("切線段 ＝ √（OA<sup>2</sup> ＋ OP<sup>2</sup>）", "OP 是斜邊：√（OP<sup>2</sup> － OA<sup>2</sup>）"),
         ("距離等於半徑時點在圓內", "等於時在圓上")])
    faq = [{"q": "為什麼切線一定垂直半徑？",
            "a": "切點是直線上離圓心最近的點，從一點到直線最短的線段是垂線，所以過切點的半徑垂直切線。"},
           {"q": "弦心距有什麼用？",
            "a": "弦心距垂直平分弦，形成直角三角形：半徑是斜邊，半弦和弦心距是兩股，知道兩個就能求第三個。"},
           {"q": "九年級的點、線、圓關係要學什麼？",
            "a": "108課綱 S-9-7：點與圓、直線與圓的位置關係，切線性質，弦心距垂直平分弦；S-9-6 中的切線段等長。"}]
    make_unit(R, "grade-9", "points-lines-and-circles", "S-9-7",
              "點、直線與圓的關係：點與圓的位置關係（內部、圓上、外部）；直線與圓的位置關係（不相交、相切、交於兩點）；圓心與切點的連線垂直此切線（切線性質）；圓心到弦的垂直線段（弦心距）垂直平分此弦。",
              "點、直線與圓：切線與弦心距",
              "九年級數學 圓的切線與弦心距 練習題｜點線圓位置・切線段等長 學習單（附解答）",
              "切線與弦心距",
              "國中九年級數學「點、直線與圓：切線與弦心距」免費學習單：點、直線和圓的位置關係、切線垂直半徑、弦心距垂直平分弦、切線段等長、拱橋與輪子應用題。100題線上練習馬上對答案，附可列印解答。",
              "切線垂直半徑，弦心距垂直平分弦",
              "從圓外一點到圓的兩條切線段等長。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
