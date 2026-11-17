# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：比長短（108課綱 N-1-5）
  python3 tools/gen_tw_math_g1_comparing_length.py
直接比較（端をそろえた鉛筆）、端がそろっていないときの注意、個別單位（積木・迴紋針幾個長）で測る、間接比較（ひもで比べる）、積木の塔の高さ、單位が違うと比べられない。
誤答：端をそろえずに右端だけで比べる、單位の數だけで比べる（大きい單位を忘れる）、長いほうと短いほうの取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81209)
NM = Names(R)
L4 = "甲乙丙丁"


def s1(seen):
    def mk():
        n = R.choice([3, 4])
        ls = R.sample(range(2, 9), n)
        k = R.choice(["長", "短"])
        i = ls.index(max(ls) if k == "長" else min(ls))
        q = "哪一枝鉛筆最%s？" % k + P.pencils(ls, list(L4[:n]))
        return mcq(q, L4[i], [L4[j] for j in range(n) if j != i] + (["一樣長"] if n < 4 else []), "左邊對齊了，看右邊誰%s：%s最%s。" % ("最遠" if k == "長" else "最近", L4[i], k))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.sample(range(3, 10), 2)
        q = "用積木量長度：甲是 %d 個積木長，乙是 %d 個積木長。哪一個比較長？長幾個積木？" % (a, b)
        L = "甲" if a > b else "乙"
        d = abs(a - b)
        return mcq(q, "%s，長 %d 個" % (L, d), ["%s，長 %d 個" % ("乙" if L == "甲" else "甲", d), "%s，長 %d 個" % (L, a + b), "一樣長"], "%d 和 %d 比，%s比較長，%d － %d ＝ %d 個。" % (a, b, L, max(a, b), min(a, b), d))

    def tower():
        hs = R.sample(range(2, 9), 3)
        k = R.choice(["高", "矮"])
        i = hs.index(max(hs) if k == "高" else min(hs))
        q = "哪一座積木塔最%s？" % k + P.towers(hs, list("甲乙丙"))
        return mcq(q, "甲乙丙"[i], [x for x in "甲乙丙" if x != "甲乙丙"[i]] + ["一樣高"], "數一數積木：%s。%s最%s。" % ("、".join("%s %d 個" % ("甲乙丙"[j], hs[j]) for j in range(3)), "甲乙丙"[i], k))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, tower, 10, seen)


def s3(seen):
    def mk():
        u = R.choice([("迴紋針", "個"), ("橡皮擦", "個"), ("鉛筆", "枝"), ("手掌", "個")])
        a, b = R.sample(range(3, 15), 2)
        x, y = R.sample(["課本", "鉛筆盒", "桌子", "門", "書包", "尺"], 2)
        q = "用%s量：%s長 %d %s%s，%s長 %d %s%s。哪一個比較長？" % (u[0], x, a, u[1], u[0], y, b, u[1], u[0])
        ans = x if a > b else y
        return mcq(q, ans, [y if ans == x else x, "一樣長", "不能比"], "用一樣的東西量，數量多的比較長：%d %s %d。" % (a, "＞" if a > b else "＜", b))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    FACTS = [("小明用迴紋針量桌子是 12 個長，小美用鉛筆量是 5 枝長。可以說小明量的比較長嗎？", "不能，量的東西不一樣", ["可以，12 比 5 大", "可以，迴紋針比較長", "不能，要再量一次"], "用的單位不同（迴紋針和鉛筆不一樣長），不能只看數量比。"),
             ("兩條繩子彎彎的放在桌上，怎麼比哪一條比較長？", "把繩子拉直，一端對齊再比", ["看哪一條看起來比較大", "比哪一條比較粗", "數一數彎了幾次"], "長度要拉直、一端對齊才能比。"),
             ("兩枝鉛筆沒有對齊，怎麼比長短？", "把一端對齊再看另一端", ["看右邊哪一枝比較遠", "看顏色", "看哪一枝比較新"], "直接比較時要先把一端對齊。"),
             ("桌子太大搬不動，怎麼比桌子的長和門的寬？", "用一條繩子量桌子，再拿繩子去比門", ["用眼睛看", "把門拆下來", "不能比"], "用繩子當中間的東西，間接比較。"),
             ("用一樣長的積木量，甲是 6 個長，乙是 6 個長。誰比較長？", "一樣長", ["甲", "乙", "不能比"], "一樣的積木，數量一樣，長度就一樣。"),
             ("量長度時，迴紋針要怎麼排？", "一個接一個，中間不留空也不重疊", ["隨便排", "排成圓圈", "留一點空"], "量的時候要頭尾相接，不能有空隙或重疊。"),
             ("同一張桌子，用迴紋針量和用鉛筆量，哪一個的數量比較多？", "用迴紋針量", ["用鉛筆量", "一樣多", "不知道"], "迴紋針比較短，要用比較多個才排得滿。"),
             ("用腳步量教室，大人走了 10 步，小朋友走了 15 步。為什麼不一樣？", "大人的步伐比較大", ["小朋友走錯了", "教室變大了", "大人走得比較快"], "單位（步伐）大小不同，量出來的數量就不同。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def compare3():
        a, b, c = R.sample(range(4, 15), 3)
        x, y, z = NM.next(), NM.next(), NM.next()
        q = "%s的跳繩 %d 個手掌長，%s的 %d 個手掌長，%s的 %d 個手掌長（用同一個人的手掌量）。誰的跳繩最長？" % (x, a, y, b, z, c)
        m = max(a, b, c)
        ans = [x, y, z][[a, b, c].index(m)]
        return mcq(q, ans, [n for n in (x, y, z) if n != ans] + ["一樣長"], "用同一個手掌量，數量最多的最長：%d。" % m)
    return out + pick_unique(R, compare3, 12, seen)


def s5(seen):
    def diff():
        a, b = R.sample(range(5, 20), 2)
        x, y = NM.next(), NM.next()
        q = "用積木量：%s的鉛筆盒 %d 個積木長，%s的 %d 個積木長。誰的比較長？長幾個積木？" % (x, a, y, b)
        ans = x if a > b else y
        d = abs(a - b)
        return mcq(q, "%s，長 %d 個" % (ans, d), ["%s，長 %d 個" % (y if ans == x else x, d), "%s，長 %d 個" % (ans, a + b), "%s，長 %d 個" % (ans, d + 1)], "%d － %d ＝ %d。" % (max(a, b), min(a, b), d))

    def sumu():
        a, b = R.randint(2, 9), R.randint(2, 9)
        q = "一條緞帶先量了 %d 個迴紋針長，剩下的又量了 %d 個迴紋針長。整條緞帶是幾個迴紋針長？" % (a, b)
        return mcq(q, "%d 個" % (a + b), ["%d 個" % x for x in (abs(a - b) if a != b else a + b + 1, a + b + 1, max(a, b))], "%d ＋ %d ＝ %d。" % (a, b, a + b))
    return pick_unique(R, diff, 12, seen) + pick_unique(R, sumu, 8, seen)


def main():
    seen = set()
    sets = [("比一比哪一枝長", s1(seen)), ("用積木量", s2(seen)), ("用東西當單位", s3(seen)),
            ("怎麼比才公平", s4(seen)), ("長多少", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>直接比</b>：把一端對齊，看另一端誰比較遠。" + P.pencils([6, 4], ["甲", "乙"]),
         "<b>用東西當單位量</b>：用迴紋針、積木、手掌一個接一個排，數有幾個。用<b>一樣的東西</b>量，數量多的比較長。",
         "不能直接放在一起比時，可以用繩子先量一個，再去比另一個（<b>間接比</b>）。"],
        [example("甲 7 個積木長，乙 4 個積木長", ["7 比 4 多 3。"], "甲長 3 個積木"),
         example("用迴紋針量 10 個，用鉛筆量 3 枝", ["單位不一樣，不能只看數量。"], "不能比")],
        [("沒對齊就看右邊", "要先把一端對齊"),
         ("迴紋針 12 個比鉛筆 5 枝長", "單位不同不能比"),
         ("量的時候留空隙", "要一個接一個")])
    faq = [{"q": "一年級為什麼還不學公分？",
            "a": "108課綱 N-1-5：一年級先用操作學直接比較、間接比較和用個別單位量，二年級才認識公分和尺。"},
           {"q": "什麼是個別單位？",
            "a": "用迴紋針、積木、手掌等一樣大的東西當單位，數有幾個，就知道有多長。"},
           {"q": "為什麼不同人用手掌量會不一樣？",
            "a": "每個人的手掌大小不同，單位不一樣，所以後來才需要大家都一樣的「公分」。"}]
    make_unit(R, "grade-1", "comparing-length", "N-1-5",
              "長度（同 M-1-1）：以操作活動為主。初步認識、直接比較、間接比較（含個別單位）。",
              "比長短：直接比和用單位量",
              "一年級數學 比長短 練習題｜直接比較・個別單位・間接比較 學習單（附解答）",
              "比長短",
              "國小一年級數學「比長短」免費學習單：對齊比長短、用積木和迴紋針量、用同樣的東西當單位、怎麼比才公平、長多少。100題線上練習，題目短、圖多，附可列印解答。",
              "一端對齊再比；用一樣的東西量",
              "單位不一樣，不能只看數量比。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
