# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：容量「公升」「毫升」（108課綱 N-3-15）
  python3 tools/gen_tw_math_g3_liters_and_milliliters.py
量杯の報讀、1 公升＝1000 毫升の換算、比大小、容量の加減、量感と應用問題。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g3_measure import bs, beaker

R = random.Random(31015)
NM = Names(R)


def L(v):
    return bs(v, "公升", "毫升")


def s1(seen):
    def mk():
        top, step, lab = R.choice([(1000, 100, 200), (1000, 50, 200), (500, 50, 100), (1000, 100, 500)])
        k = R.randint(1, top // step - 1)
        v = k * step
        if v % lab == 0 and R.random() < .6:
            return None
        q = "量杯裡的水有多少毫升？" + beaker(v, top, step, lab)
        n_lab = lab // step
        return mcq(q, "%d 毫升" % v, ["%d 毫升" % x for x in (k * 10 if k * 10 != v else v + 2 * step, v + step, v - step, k * 100 if k * 100 != v else v + lab)],
                   "從 0 到 %d 有 %d 小格，1 小格是 %d 毫升。水到第 %d 格：%d 毫升。" % (lab, n_lab, step, k, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def to_s():
        b = R.randint(1, 9)
        s = R.choice([R.randint(1, 9) * 100, R.randint(1, 9) * 100 + R.randint(1, 9) * 10, R.randint(1, 9) * 10, R.randint(1, 9) * 100 + 5])
        v = b * 1000 + s
        q = "%d 公升 %d 毫升 ＝ ___ 毫升" % (b, s)
        return mcq(q, str(v), [str(x) for x in (int("%d%d" % (b, s)), b * 10000 + s, v + 1000, v - 1000 if b > 1 else v + 2000, b * 100 + s) if x != v],
                   "1 公升 ＝ 1000 毫升，%s再加 %d：%d 毫升。" % ("%d 公升 ＝ %d 毫升，" % (b, b * 1000) if b > 1 else "", s, v))

    def to_b():
        v = R.randint(1, 9) * 1000 + R.choice([R.randint(1, 9) * 100, R.randint(11, 99) * 10, R.randint(1, 9) * 10])
        b, s = divmod(v, 1000)
        if s == 0:
            return None
        q = "%d 毫升 ＝ ___ 公升 ___ 毫升" % v
        st = str(v)
        return mcq(q, L(v), ["%d 公升 %d 毫升" % x for x in ((int(st[:2]), int(st[2:]) or 1), (b, s // 10 if s % 10 == 0 and s >= 100 else s + 100), (b + 1, s), (b - 1, s + 1000) if b > 1 else (b, s * 10 if s < 100 else s + 10))],
                   "每 1000 毫升是 1 公升：%d 毫升 ＝ %d 公升 %d 毫升。" % (v, b, s))

    def whole():
        b = R.randint(2, 15)
        if R.random() < .5:
            return mcq("%d 公升 ＝ ___ 毫升" % b, str(b * 1000), [str(x) for x in (b * 100, b * 10, b * 10000)],
                       "1 公升 ＝ 1000 毫升，%d 公升 ＝ %d 毫升。" % (b, b * 1000))
        return mcq("%d 毫升 ＝ ___ 公升" % (b * 1000), str(b), [str(x) for x in (b * 10, b * 100, b * 1000)],
                   "1000 毫升 ＝ 1 公升，%d 毫升 ＝ %d 公升。" % (b * 1000, b))
    return pick_unique(R, to_s, 8, seen) + pick_unique(R, to_b, 7, seen) + pick_unique(R, whole, 5, seen)


def s3(seen):
    def mk():
        a = R.randint(1, 5) * 1000 + R.randint(1, 19) * 50
        b = a + R.choice([-900, -450, -100, 50, 200, 800, 1000])
        if b <= 0 or b % 1000 == a % 1000:
            return None
        q = "%s ○ %d 毫升，○ 裡要填什麼？" % (L(a), b)
        sign = ">" if a > b else "<"
        return mcq(q, sign, ["<" if sign == ">" else ">", "=", "無法比較"], "%s ＝ %d 毫升，%d %s %d。" % (L(a), a, a, sign, b))

    def most():
        vs = R.sample(range(800, 3200, 50), 4)
        if len({v // 100 for v in vs}) < 4:
            return None
        labs = [L(v) if i % 2 == 0 else "%d 毫升" % v for i, v in enumerate(vs)]
        ans = labs[vs.index(max(vs))]
        return mcq("哪一個容量最多？" + "、".join(labs), ans, [x for x in labs if x != ans], "都換成毫升再比：最多的是 %d 毫升。" % max(vs))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, most, 8, seen)


def s4(seen):
    def add():
        a = R.randint(1, 4) * 1000 + R.randint(1, 9) * 100
        b = R.randint(0, 3) * 1000 + R.randint(1, 9) * 100
        if (a % 1000 + b % 1000) < 1000 and R.random() < .6:
            return None
        s = a + b
        q = "%s ＋ %s ＝" % (L(a), L(b))
        w = ["%d 公升 %d 毫升" % (a // 1000 + b // 1000, a % 1000 + b % 1000), L(s + 1000), L(s - 1000), L(s + 100)]
        return mcq(q, L(s), w, "公升加公升、毫升加毫升，滿 1000 毫升換成 1 公升：%s。" % L(s))

    def sub():
        a = R.randint(2, 6) * 1000 + R.randint(0, 9) * 100
        b = R.randint(0, a // 1000 - 1) * 1000 + R.randint(1, 9) * 100
        d = a - b
        if d % 1000 == 0 or d <= 0:
            return None
        q = "%s － %s ＝" % (L(a), L(b))
        w = ["%d 公升 %d 毫升" % (a // 1000 - b // 1000, abs(a % 1000 - b % 1000)) if a % 1000 != b % 1000 else L(d + 200), L(d + 1000), L(d - 1000) if d > 1000 else L(d + 2000), L(d + 100)]
        return mcq(q, L(d), w, "毫升不夠減，向公升借 1 公升 ＝ 1000 毫升：%s。" % L(d))
    return pick_unique(R, add, 10, seen) + pick_unique(R, sub, 10, seen)


def s5(seen):
    SENSE = [("一瓶家庭號鮮奶", "2", "公升"), ("一罐養樂多", "100", "毫升"), ("一個馬克杯裝滿水", "300", "毫升"),
             ("一個大水桶裝滿水", "10", "公升"), ("一湯匙的藥水", "5", "毫升"), ("一瓶寶特瓶礦泉水", "600", "毫升"),
             ("浴缸裝滿水", "200", "公升"), ("一罐鋁箔包豆漿", "250", "毫升")]
    out = []
    for it, n, u in SENSE:
        out.append(mcq("%s大約是 %s ___，填哪一個單位最合適？" % (it, n), u, [x for x in ("公升", "毫升", "公斤", "公分") if x != u],
                       "想一想實際有多少：%s大約 %s %s。" % (it, n, u)))
    for b in out:
        seen.add(b["q"])

    def word():
        who = NM.next()
        kind = R.choice(["pour", "cups", "two"])
        if kind == "pour":
            a = R.choice([1500, 2000, 1250, 1800, 2400])
            d = R.randint(2, 9) * 100 + R.choice([0, 50])
            q = "一壺麥茶有 %s，倒出 %d 毫升，還剩多少？" % (L(a), d)
            r = a - d
            return mcq(q, L(r), [L(a + d), L(r + 1000) if r + 1000 != a else L(r + 500), L(r - 100), "%d 毫升" % (a // 1000 * 100 + a % 1000 - d) if a // 1000 * 100 + a % 1000 > d else L(r + 100)],
                       "%s ＝ %d 毫升，%d － %d ＝ %d 毫升 ＝ %s。" % (L(a), a, a, d, r, L(r)))
        if kind == "cups":
            c = R.choice([200, 250, 300, 150])
            n = R.randint(3, 8)
            q = "一杯果汁 %d 毫升，%s倒了 %d 杯，一共多少毫升？" % (c, who, n)
            t = c * n
            return mcq(q, "%d 毫升" % t if t < 1000 else "%d 毫升（%s）" % (t, L(t)),
                       ["%d 毫升" % x if x < 1000 else "%d 毫升（%s）" % (x, L(x)) for x in (c + n, t + c, t - c, t * 10)],
                       "%d × %d ＝ %d（毫升）。" % (c, n, t))
        a, b = R.randint(3, 9) * 100, R.randint(3, 9) * 100 + 50
        o = NM.next()
        if o == who:
            return None
        q = "%s的水壺裝了 %d 毫升的水，%s的水壺裝了 %d 毫升。兩人一共有多少水？" % (who, a, o, b)
        t = a + b
        return mcq(q, L(t), [L(abs(a - b)), "%d 公升 %d 毫升" % (t // 100, t % 100) if t % 100 else L(t + 100), L(t + 1000), L(t - 100)],
                   "%d ＋ %d ＝ %d（毫升），%s。" % (a, b, t, "就是 " + L(t) if t >= 1000 else "不到 1 公升"))
    return out + pick_unique(R, word, 12, seen)


def main():
    seen = set()
    sets = [("讀量杯", s1(seen)), ("公升和毫升的換算", s2(seen)), ("比多少", s3(seen)),
            ("容量的加減", s4(seen)), ("量感和應用問題", s5(seen))]
    demo = beaker(600, 1000, 100, 200)
    body = lesson(
        ["<b>容量</b>是容器能裝多少液體。大的單位是<b>公升</b>，小的單位是<b>毫升</b>。",
         "<b>1 公升 ＝ 1000 毫升</b>。2 公升 50 毫升 ＝ 2000 ＋ 50 ＝ 2050 毫升。",
         "讀量杯：先看 1 小格是多少毫升，再看水面對到哪一格。"],
        [example("量杯裡有多少毫升？" + demo, ["0 到 200 有 2 小格，1 小格是 100 毫升。", "水面在第 6 格。"], "600 毫升"),
         example("1 公升 600 毫升 ＋ 700 毫升 ＝", ["毫升：600 ＋ 700 ＝ 1300，1300 毫升 ＝ 1 公升 300 毫升。", "公升：1 ＋ 1 ＝ 2。"], "2 公升 300 毫升")],
        [("2 公升 50 毫升 ＝ 250 毫升", "2 公升是 2000 毫升：2000 ＋ 50 ＝ 2050 毫升"),
         ("1 公升 ＝ 100 毫升", "1 公升 ＝ 1000 毫升"),
         ("答案寫成 1 公升 1300 毫升", "滿 1000 毫升要換成 1 公升：2 公升 300 毫升")])
    faq = [{"q": "1 公升等於幾毫升？",
            "a": "1 公升 ＝ 1000 毫升。一瓶家庭號鮮奶大約 2 公升，一罐養樂多大約 100 毫升。"},
           {"q": "三年級的容量單元要學什麼？",
            "a": "108課綱 N-3-15：認識公升和毫升，會用量杯實際測量、估測容量，做單位換算和加減計算。"},
           {"q": "孩子換算時常漏掉 0，怎麼辦？",
            "a": "提醒「毫升要寫成 4 位數」：2 公升 50 毫升 → 2 □□□，填成 2050，不夠的位寫 0。"}]
    make_unit(R, "grade-3", "liters-and-milliliters", "N-3-15",
              "容量：「公升」、「毫升」。實測、量感、估測與計算。單位換算。",
              "容量：公升和毫升",
              "三年級數學 公升和毫升 練習題｜讀量杯・容量換算・容量加減 學習單（附解答）",
              "公升和毫升",
              "國小三年級數學「公升和毫升」免費學習單：讀量杯、1公升＝1000毫升的換算、比多少、容量加減與量感應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 公升 ＝ 1000 毫升",
              "滿 1000 毫升換成 1 公升；換算時毫升寫成 4 位數。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
