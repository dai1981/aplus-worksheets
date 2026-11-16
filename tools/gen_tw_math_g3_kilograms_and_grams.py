# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：重量「公斤」「公克」（108課綱 N-3-16）
  python3 tools/gen_tw_math_g3_kilograms_and_grams.py
秤の報讀、1 公斤＝1000 公克の換算、比輕重、重量の加減、量感と應用問題。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g3_measure import bs, dial

R = random.Random(31016)
NM = Names(R)


def K(v):
    return bs(v, "公斤", "公克")


def s1(seen):
    def small():
        k = R.randint(1, 9)
        g = k * 100
        q = "秤上的東西有多重？" + dial(g, 1000)
        return mcq(q, "%d 公克" % g, ["%d 公克" % x for x in (k * 10, g + 100, g - 100 if g > 100 else g + 200, 1000 - g if 1000 - g != g else g + 300)],
                   "一圈是 1000 公克，分成 10 小格，1 小格是 100 公克。指針在第 %d 格：%d 公克。" % (k, g))

    def big():
        top = R.choice([2000, 3000, 4000])
        k = R.randint(1, top // 100 - 1)
        g = k * 100
        if g % 1000 == 0:
            return None
        q = "秤上的東西有多重？" + dial(g, top)
        return mcq(q, K(g), [K(x) for x in (g + 100, g - 100, g + 1000 if g + 1000 < top else g - 1000 if g > 1000 else g + 200)] + ["%d 公斤 %d 公克" % (g // 1000, g % 1000 // 100)],
                   "1 公斤之間有 10 小格，1 小格是 100 公克。指針過了 %d 公斤，再多 %d 小格：%s。" % (g // 1000, g % 1000 // 100, K(g)))
    return pick_unique(R, small, 8, seen) + pick_unique(R, big, 12, seen)


def s2(seen):
    def to_s():
        b = R.randint(1, 9)
        s = R.choice([R.randint(1, 9) * 100, R.randint(11, 99) * 10, R.randint(1, 9) * 10, R.randint(101, 999)])
        v = b * 1000 + s
        q = "%d 公斤 %d 公克 ＝ ___ 公克" % (b, s)
        return mcq(q, str(v), [str(x) for x in (int("%d%d" % (b, s)), b * 10000 + s, v + 1000, v - 1000 if b > 1 else v + 2000, b * 100 + s) if x != v],
                   "1 公斤 ＝ 1000 公克，%s再加 %d：%d 公克。" % ("%d 公斤 ＝ %d 公克，" % (b, b * 1000) if b > 1 else "", s, v))

    def to_b():
        v = R.randint(1, 9) * 1000 + R.choice([R.randint(1, 9) * 100, R.randint(11, 99) * 10, R.randint(1, 9) * 10, R.randint(101, 999)])
        b, s = divmod(v, 1000)
        st = str(v)
        return mcq("%d 公克 ＝ ___ 公斤 ___ 公克" % v, K(v),
                   ["%d 公斤 %d 公克" % x for x in ((int(st[:2]), int(st[2:]) or 1), (b + 1, s), (b, s + 100), (b - 1, s + 1000) if b > 1 else (b, s * 10 if s < 100 else s + 10))],
                   "每 1000 公克是 1 公斤：%d 公克 ＝ %s。" % (v, K(v)))

    def whole():
        b = R.randint(2, 20)
        if R.random() < .5:
            return mcq("%d 公斤 ＝ ___ 公克" % b, str(b * 1000), [str(x) for x in (b * 100, b * 10, b * 10000)], "1 公斤 ＝ 1000 公克，%d 公斤 ＝ %d 公克。" % (b, b * 1000))
        return mcq("%d 公克 ＝ ___ 公斤" % (b * 1000), str(b), [str(x) for x in (b * 10, b * 100, b * 1000)], "1000 公克 ＝ 1 公斤，%d 公克 ＝ %d 公斤。" % (b * 1000, b))
    return pick_unique(R, to_s, 8, seen) + pick_unique(R, to_b, 7, seen) + pick_unique(R, whole, 5, seen)


def s3(seen):
    def mk():
        a = R.randint(1, 8) * 1000 + R.randint(1, 19) * 50
        b = a + R.choice([-900, -450, -100, 50, 200, 800, 1000])
        if b <= 0 or b % 1000 == a % 1000:
            return None
        sign = ">" if a > b else "<"
        return mcq("%s ○ %d 公克，○ 裡要填什麼？" % (K(a), b), sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "%s ＝ %d 公克，%d %s %d。" % (K(a), a, a, sign, b))

    def light():
        vs = R.sample(range(600, 3200, 50), 4)
        if len({v // 100 for v in vs}) < 4:
            return None
        labs = [K(v) if i % 2 == 0 else "%d 公克" % v for i, v in enumerate(vs)]
        ask = R.choice(["最重", "最輕"])
        t = max(vs) if ask == "最重" else min(vs)
        ans = labs[vs.index(t)]
        return mcq("哪一個%s？" % ask + "、".join(labs), ans, [x for x in labs if x != ans], "都換成公克再比：%s的是 %d 公克。" % (ask, t))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, light, 8, seen)


def s4(seen):
    def add():
        a = R.randint(1, 5) * 1000 + R.randint(1, 19) * 50
        b = R.randint(0, 3) * 1000 + R.randint(1, 19) * 50
        if (a % 1000 + b % 1000) < 1000 and R.random() < .6:
            return None
        s = a + b
        w = ["%d 公斤 %d 公克" % (a // 1000 + b // 1000, a % 1000 + b % 1000), K(s + 1000), K(s - 1000), K(s + 100), K(s - 100)]
        return mcq("%s ＋ %s ＝" % (K(a), K(b)), K(s), w, "公斤加公斤、公克加公克，滿 1000 公克換成 1 公斤：%s。" % K(s))

    def sub():
        a = R.randint(2, 8) * 1000 + R.randint(0, 19) * 50
        b = R.randint(0, a // 1000 - 1) * 1000 + R.randint(1, 19) * 50
        d = a - b
        if d % 1000 == 0 or d <= 0:
            return None
        w = ["%d 公斤 %d 公克" % (a // 1000 - b // 1000, abs(a % 1000 - b % 1000)) if a % 1000 != b % 1000 else K(d + 200), K(d + 1000), K(d - 1000) if d > 1000 else K(d + 2000), K(d + 100), K(d - 50)]
        return mcq("%s － %s ＝" % (K(a), K(b)), K(d), w, "公克不夠減，向公斤借 1 公斤 ＝ 1000 公克：%s。" % K(d))
    return pick_unique(R, add, 10, seen) + pick_unique(R, sub, 10, seen)


def s5(seen):
    SENSE = [("一顆雞蛋", "60", "公克"), ("一個三年級學生的體重", "28", "公斤"), ("一大包米", "5", "公斤"),
             ("一枚 1 元硬幣", "4", "公克"), ("一顆西瓜", "6", "公斤"), ("一本數學課本", "300", "公克"),
             ("一個書包裝滿課本", "4", "公斤"), ("一顆蘋果", "250", "公克")]
    out = []
    for it, n, u in SENSE:
        out.append(mcq("%s大約是 %s ___，填哪一個單位最合適？" % (it, n), u, [x for x in ("公斤", "公克", "公升", "公分") if x != u],
                       "想一想拿起來有多重：%s大約 %s %s。" % (it, n, u)))
    for b in out:
        seen.add(b["q"])

    def word():
        who = NM.next()
        kind = R.choice(["bag", "same", "box"])
        if kind == "bag":
            a = R.randint(2, 5) * 1000 + R.randint(1, 9) * 100
            b = R.randint(3, 9) * 100
            q = "%s的書包重 %s，放進一個 %d 公克的便當盒後，一共重多少？" % (who, K(a), b)
            s = a + b
            return mcq(q, K(s), ["%d 公斤 %d 公克" % (a // 1000, a % 1000 + b) if a % 1000 + b >= 1000 else K(s + 1000), K(a - b), K(s + 100), K(s - 1000)],
                       "%d ＋ %d ＝ %d（公克）＝ %s。" % (a, b, s, K(s)))
        if kind == "same":
            g = R.choice([150, 200, 250, 300, 125])
            n = R.randint(3, 8)
            item = R.choice(["蘋果", "芭樂", "柳丁"])
            q = "一顆%s大約 %d 公克，%d 顆大約多重？" % (item, g, n)
            t = g * n
            return mcq(q, K(t), [K(x) for x in (g + n, t + g, t - g, t * 10)], "%d × %d ＝ %d（公克）%s。" % (g, n, t, "＝ " + K(t) if t >= 1000 else ""))
        a = R.randint(3, 9) * 1000 + R.randint(1, 9) * 100
        b = R.randint(1, a // 1000 - 1) * 1000 + R.randint(1, 9) * 100
        q = "一箱橘子重 %s，賣掉 %s，還剩多重？" % (K(a), K(b))
        d = a - b
        if d % 1000 == 0:
            return None
        return mcq(q, K(d), [K(a + b), "%d 公斤 %d 公克" % (a // 1000 - b // 1000, abs(a % 1000 - b % 1000)) if a % 1000 != b % 1000 else K(d + 100), K(d + 1000), K(d - 100)],
                   "%s － %s ＝ %s。" % (K(a), K(b), K(d)))
    return out + pick_unique(R, word, 12, seen)


def main():
    seen = set()
    sets = [("讀秤", s1(seen)), ("公斤和公克的換算", s2(seen)), ("比輕重", s3(seen)),
            ("重量的加減", s4(seen)), ("量感和應用問題", s5(seen))]
    demo = dial(1300, 3000)
    body = lesson(
        ["<b>重量</b>的大單位是<b>公斤</b>，小單位是<b>公克</b>。",
         "<b>1 公斤 ＝ 1000 公克</b>。3 公斤 80 公克 ＝ 3000 ＋ 80 ＝ 3080 公克。",
         "讀秤：先看 1 小格是多少公克，再從指針前面的公斤數往後數。"],
        [example("秤上的東西有多重？" + demo, ["1 公斤之間有 10 小格，1 小格是 100 公克。", "指針過了 1 公斤，再多 3 小格。"], "1 公斤 300 公克"),
         example("2 公斤 700 公克 ＋ 500 公克 ＝", ["公克：700 ＋ 500 ＝ 1200，1200 公克 ＝ 1 公斤 200 公克。", "公斤：2 ＋ 1 ＝ 3。"], "3 公斤 200 公克")],
        [("3 公斤 80 公克 ＝ 380 公克", "3 公斤是 3000 公克：3000 ＋ 80 ＝ 3080 公克"),
         ("1 公斤 ＝ 100 公克", "1 公斤 ＝ 1000 公克"),
         ("東西看起來大就比較重", "要用秤量；換成同一個單位再比")])
    faq = [{"q": "1 公斤等於幾公克？",
            "a": "1 公斤 ＝ 1000 公克。一顆雞蛋大約 60 公克，一包米常見 1、3、5 公斤裝。"},
           {"q": "三年級的重量單元要學什麼？",
            "a": "108課綱 N-3-16：認識公斤和公克，會用秤實際測量、估測重量，做單位換算和加減計算。"},
           {"q": "怎麼讓孩子對公斤、公克有感覺？",
            "a": "在家用廚房秤量水果、書包，先猜再量；記住雞蛋約 60 公克、1 公升的水約 1 公斤，估測就會越來越準。"}]
    make_unit(R, "grade-3", "kilograms-and-grams", "N-3-16",
              "重量：「公斤」、「公克」。實測、量感、估測與計算。單位換算。",
              "重量：公斤和公克",
              "三年級數學 公斤和公克 練習題｜讀秤・重量換算・重量加減 學習單（附解答）",
              "公斤和公克",
              "國小三年級數學「公斤和公克」免費學習單：讀秤、1公斤＝1000公克的換算、比輕重、重量加減與量感應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 公斤 ＝ 1000 公克",
              "滿 1000 公克換成 1 公斤；換算時公克寫成 4 位數。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
