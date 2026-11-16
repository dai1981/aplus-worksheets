# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：旋轉角（108課綱 S-4-2）
  python3 tools/gen_tw_math_g4_rotation.py
鐘面で：分針が數字から數字へ回る角度、經過時間と分針の角度、時針の角度、順時針・逆時針、方位の向きの変化。
誤答：1 格を 5 度とする（數字 1 つは 30 度）、逆向きに数える、平角と周角の取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, clock

R = random.Random(41012)
NM = Names(R)
DIRS = ["北", "東", "南", "西"]


def s1(seen):
    def mk():
        a = R.randint(1, 12)
        k = R.randint(1, 11)
        cw = R.random() < .7
        b = (a + k - 1) % 12 + 1 if cw else (a - k - 1) % 12 + 1
        q = "長針從 %d %s轉到 %d，轉了幾度？" % (a, "順時針" if cw else "逆時針", b)
        v = 30 * k
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (360 - v if v != 180 else 90, 5 * k, v + 30, v - 30 if v > 30 else v + 60)],
                   "鐘面一圈 360 度，分成 12 大格，1 大格是 30 度。%s轉了 %d 大格：30 × %d ＝ %d（度）。" % ("順時針" if cw else "逆時針", k, k, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        m = R.choice(range(5, 60, 5))
        v = m * 6
        q = "經過 %d 分鐘，分針轉了幾度？" % m
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (m, m * 30 if m * 30 != v else v + 30, v + 30, 360 - v if v != 180 else 90)],
                   "分針 60 分鐘轉一圈 360 度，1 分鐘轉 6 度（5 分鐘轉 30 度）：%d × 6 ＝ %d（度）。" % (m, v))

    def back():
        v = R.choice([30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])
        m = v // 6
        q = "分針順時針轉了 %d 度，經過了幾分鐘？" % v
        return mcq(q, "%d 分鐘" % m, ["%d 分鐘" % x for x in (v // 30, v // 10, m + 5, 60 - m if 60 - m != m else m + 10)], "1 分鐘轉 6 度：%d ÷ 6 ＝ %d（分鐘）。" % (v, m))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, back, 10, seen)


def s3(seen):
    def hour():
        h = R.randint(1, 11)
        s0 = R.randint(1, 12)
        q = "從 %d 點到 %d 點，時針轉了幾度？" % (s0, (s0 + h - 1) % 12 + 1)
        return mcq(q, "%d 度" % (30 * h), ["%d 度" % x for x in (6 * h, 360 * h if h < 2 else 15 * h, 30 * h + 30, 360 - 30 * h if 360 - 30 * h != 30 * h else 30 * h - 30)],
                   "經過 %d 小時。時針 12 小時轉一圈，1 小時轉 30 度：30 × %d ＝ %d（度）。" % (h, h, 30 * h))

    def hands():
        h = R.randint(1, 11)
        q = "%d 點整時，時針和分針形成的角（較小的那一個）是幾度？" % h + clock(h, 0, 150)
        v = 30 * min(h, 12 - h)
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (360 - v, 30 * h if 30 * h != v else v + 30, v + 30, 5 * h, v - 30)],
                   "分針指 12，時針指 %d，中間有 %d 大格：30 × %d ＝ %d（度）。" % (h, min(h, 12 - h), min(h, 12 - h), v))
    return pick_unique(R, hour, 10, seen) + pick_unique(R, hands, 10, seen)


def s4(seen):
    def land():
        a = R.randint(1, 12)
        deg = R.choice([30, 60, 90, 120, 150, 180, 270])
        cw = R.random() < .5
        k = deg // 30
        b = (a + k - 1) % 12 + 1 if cw else (a - k - 1) % 12 + 1
        o = (a - k - 1) % 12 + 1 if cw else (a + k - 1) % 12 + 1
        q = "長針指著 %d，%s轉 %d 度後指著幾？" % (a, "順時針" if cw else "逆時針", deg)
        cands = ["指著 %d" % x for x in (o, (b % 12) + 1, ((b - 2) % 12) + 1, (a + deg // 5 - 1) % 12 + 1) if x != b]
        return mcq(q, "指著 %d" % b, cands, "%d 度是 %d 大格。%s從 %d 數 %d 格：%d。" % (deg, k, "順時針（和時鐘一樣的方向）" if cw else "逆時針（和時鐘相反的方向）", a, k, b))

    def which():
        k = R.randint(1, 11)
        if k == 6:
            return None
        a = R.randint(1, 12)
        b = (a + k - 1) % 12 + 1
        q = "長針從 %d 轉到 %d，順時針轉和逆時針轉，各轉了幾度？" % (a, b)
        v = 30 * k
        return mcq(q, "順時針 %d 度，逆時針 %d 度" % (v, 360 - v), ["順時針 %d 度，逆時針 %d 度" % x for x in ((360 - v, v), (v, 180 - v if v < 180 else v - 180), (v, v), (v, 360 - v + 30), (v - 30 if v > 30 else v + 30, 360 - v))],
                   "順時針轉 %d 大格是 %d 度；逆時針要轉另外一邊，360 － %d ＝ %d（度）。兩個合起來是一個周角。" % (k, v, v, 360 - v))
    return pick_unique(R, land, 12, seen) + pick_unique(R, which, 8, seen)


def s5(seen):
    def face():
        start = R.randrange(4)
        deg = R.choice([90, 180, 270, 360])
        right = R.random() < .5
        k = deg // 90
        end = (start + k) % 4 if right else (start - k) % 4
        who = NM.next()
        q = "%s面向%s，%s轉 %d 度（%s），現在面向哪裡？" % (who, DIRS[start], "向右" if right else "向左", deg, "順時針" if right else "逆時針")
        other = (start - k) % 4 if right else (start + k) % 4
        cands = ["面向" + DIRS[x] for x in (other, (end + 1) % 4, (end + 2) % 4, (end + 3) % 4) if x != end]
        return mcq(q, "面向" + DIRS[end], cands, "%d 度是 %d 個直角。從%s%s轉 %d 個直角：%s。%s" % (
            deg, k, DIRS[start], "向右" if right else "向左", k, DIRS[end], "轉一圈（周角）會回到原來的方向。" if deg == 360 else ""))

    def facts():
        F = [("轉半圈是幾度？", "180 度", ["90 度", "360 度", "120 度"], "半圈是一個平角，180 度。"),
             ("轉一圈是幾度？", "360 度", ["180 度", "100 度", "300 度"], "一圈是一個周角，360 度。"),
             ("和時鐘指針轉動方向一樣的叫做什麼？", "順時針", ["逆時針", "平角", "周角"], "和時鐘一樣的方向叫順時針，相反的叫逆時針。"),
             ("鐘面上相鄰的兩個數字之間是幾度？", "30 度", ["5 度", "6 度", "60 度"], "360 ÷ 12 ＝ 30（度）。"),
             ("分針從 12 轉到 6，轉了什麼角？", "平角", ["直角", "周角", "銳角"], "12 到 6 是 6 大格，30 × 6 ＝ 180 度，是平角。"),
             ("分針從 12 轉一圈又回到 12，轉了什麼角？", "周角", ["平角", "直角", "0 度"], "轉一整圈是 360 度，是周角。"),
             ("轉 3 個直角是幾度？", "270 度", ["180 度", "300 度", "90 度"], "90 × 3 ＝ 270（度）。"),
             ("時針 1 小時轉幾度？", "30 度", ["6 度", "60 度", "360 度"], "時針 12 小時轉 360 度，360 ÷ 12 ＝ 30（度）。")]
        return mcq(*R.choice(F))
    return pick_unique(R, face, 12, seen) + pick_unique(R, facts, 8, seen)


def main():
    seen = set()
    sets = [("長針轉了幾度", s1(seen)), ("分針和時間", s2(seen)), ("時針轉了幾度", s3(seen)),
            ("順時針和逆時針", s4(seen)), ("轉身和方向", s5(seen))]
    body = lesson(
        ["鐘面一圈是 360 度，分成 12 大格，<b>1 大格是 30 度</b>。",
         "和時鐘指針一樣的方向叫<b>順時針</b>，相反的方向叫<b>逆時針</b>。",
         "分針 1 分鐘轉 6 度（5 分鐘轉 30 度）；時針 1 小時轉 30 度。",
         "轉半圈是<b>平角</b>（180 度），轉一圈是<b>周角</b>（360 度）。"],
        [example("長針從 2 順時針轉到 7，轉了幾度？", ["2 到 7 是 5 大格。", "30 × 5 ＝ 150。"], "150 度"),
         example("面向北，向右轉 270 度，面向哪裡？", ["270 度是 3 個直角。", "北 → 東 → 南 → 西。"], "面向西")],
        [("1 大格當成 5 度", "1 大格（兩個數字之間）是 30 度；1 小格才是 6 度"),
         ("逆時針卻往順時針的方向數", "逆時針是和時鐘相反的方向"),
         ("轉 360 度後方向改變了", "轉一圈會回到原來的方向")])
    faq = [{"q": "旋轉角要怎麼算？",
            "a": "用鐘面來想：一圈 360 度、12 大格，1 大格 30 度。數一數從開始的邊轉到結束的邊經過幾大格，再乘以 30。"},
           {"q": "四年級的旋轉角要學什麼？",
            "a": "108課綱 S-4-2：以鐘面為模型，討論從始邊轉到終邊所轉的角度，認識順時針和逆時針兩個方向，以及平角和周角。"},
           {"q": "順時針和逆時針怎麼記？",
            "a": "順著時鐘指針轉的方向是順時針，逆著（相反）就是逆時針。同樣從 12 轉到 3：順時針 90 度，逆時針 270 度。"}]
    make_unit(R, "grade-4", "rotation", "S-4-2",
              "解題：旋轉角。以具體操作為主，並結合計算。以鐘面為模型討論從始邊轉到終邊所轉的角度。旋轉有兩個方向：「順時針」、「逆時針」。「平角」、「周角」。",
              "旋轉角：順時針和逆時針",
              "四年級數學 旋轉角 練習題｜鐘面角度・順時針逆時針 學習單（附解答）",
              "旋轉角",
              "國小四年級數學「旋轉角」免費學習單：鐘面上長針轉了幾度、分針和時針的角度、順時針和逆時針、轉身和方向。100題線上練習馬上對答案，附可列印解答。",
              "鐘面 1 大格是 30 度",
              "順時針和時鐘同方向；轉一圈 360 度。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
