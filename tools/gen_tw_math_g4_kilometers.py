# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：長度「公里」（108課綱 N-4-9）
  python3 tools/gen_tw_math_g4_kilometers.py
量感（公里・公尺・公分・毫米）、1 公里＝1000 公尺の換算、他の長さの単位換算、比較と加減、應用問題（操場、地圖、路程）。
誤答：2 公里 50 公尺 → 250 公尺、1 公里＝100 公尺、繰り上がり忘れ。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names
from tw_g3_measure import bs

R = random.Random(41010)
NM = Names(R)


def K(v):
    return bs(v, "公里", "公尺")


def s1(seen):
    SENSE = [("從台北到高雄的距離", "350", "公里"), ("學校操場跑一圈", "200", "公尺"), ("教室的長", "9", "公尺"), ("一枝鉛筆的長", "17", "公分"),
             ("走路 15 分鐘大約可以走", "1", "公里"), ("一張悠遊卡的厚度", "1", "毫米"), ("一棟 10 層樓的大樓高", "30", "公尺"),
             ("跑一場馬拉松", "42", "公里"), ("一個籃球場的長", "28", "公尺"), ("台灣南北的長度", "394", "公里")]
    out = []
    for it, n, u in SENSE:
        out.append(mcq("%s大約是 %s ___，填哪一個單位最合適？" % (it, n), u, [x for x in ("公里", "公尺", "公分", "毫米") if x != u],
                       "想一想實際有多長：%s大約 %s %s。" % (it, n, u)))
    for b in out:
        seen.add(b["q"])

    def laps():
        per = R.choice([200, 250, 400, 500])
        n = 1000 // per
        k = R.randint(2, 6)
        q = "操場跑一圈是 %d 公尺，跑幾圈剛好是 %d 公里？" % (per, k)
        v = k * 1000 // per
        if k * 1000 % per:
            return None
        return mcq(q, "%d 圈" % v, ["%d 圈" % x for x in (k * 100 // per or v + 1, v + n, v - 1, k * 10)], "%d 公里 ＝ %s 公尺，%s ÷ %d ＝ %d（圈）。" % (k, num(k * 1000), num(k * 1000), per, v))
    return out + pick_unique(R, laps, 10, seen)


def s2(seen):
    def to_m():
        b = R.randint(1, 30)
        s = R.choice([R.randint(1, 9) * 100, R.randint(11, 99) * 10, R.randint(1, 99), R.randint(101, 999)])
        v = b * 1000 + s
        return mcq("%d 公里 %d 公尺 ＝ ___ 公尺" % (b, s), num(v), [num(x) for x in (int("%d%d" % (b, s)), b * 100 + s, b * 10000 + s, v + 1000) if x != v],
                   "1 公里 ＝ 1000 公尺，%d 公里 ＝ %s 公尺，再加 %d：%s 公尺。" % (b, num(b * 1000), s, num(v)))

    def to_km():
        v = R.randint(1, 30) * 1000 + R.choice([R.randint(1, 9) * 100, R.randint(11, 99) * 10, R.randint(1, 99), R.randint(101, 999)])
        b, s = divmod(v, 1000)
        st = str(v)
        return mcq("%s 公尺 ＝ ___ 公里 ___ 公尺" % num(v), K(v),
                   ["%d 公里 %d 公尺" % x for x in ((int(st[:-2]), int(st[-2:]) or 1), (b + 1, s), (b, s + 100), (b * 10, s) if b * 10 != b else (b + 2, s))],
                   "每 1000 公尺是 1 公里：%s 公尺 ＝ %s。" % (num(v), K(v)))
    return pick_unique(R, to_m, 10, seen) + pick_unique(R, to_km, 10, seen)


def s3(seen):
    UNITS = [("公尺", "公分", 100), ("公分", "毫米", 10), ("公里", "公尺", 1000), ("公尺", "毫米", 1000)]

    def mk():
        big, small, f = R.choice(UNITS)
        n = R.randint(2, 60)
        if R.random() < .5:
            return mcq("%d %s ＝ ___ %s" % (n, big, small), num(n * f), [num(n * f * 10), num(n * f // 10), num(n * f * 100), num(n * 10) if f != 10 else num(n * 1000)],
                       "1 %s ＝ %s %s，%d %s ＝ %s %s。" % (big, num(f), small, n, big, num(n * f), small))
        return mcq("%s %s ＝ ___ %s" % (num(n * f), small, big), str(n), [str(n * 10), num(n * 100), num(n * f * 10), str(n * f // 100) if n * f // 100 not in (n, n * 10) else num(n * 1000)],
                   "%s %s ＝ 1 %s，%s %s ＝ %d %s。" % (num(f), small, big, num(n * f), small, n, big))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def cmp_():
        a = R.randint(1, 9) * 1000 + R.randint(1, 19) * 50
        b = a + R.choice([-900, -450, -100, 50, 300, 800, 1000])
        if b <= 0 or b % 1000 == a % 1000:
            return None
        sign = ">" if a > b else "<"
        return mcq("%s ○ %s 公尺，○ 裡要填什麼？" % (K(a), num(b)), sign, ["<" if sign == ">" else ">", "=", "無法比較"], "%s ＝ %s 公尺，%s %s %s。" % (K(a), num(a), num(a), sign, num(b)))

    def add():
        a = R.randint(1, 9) * 1000 + R.randint(1, 19) * 50
        b = R.randint(0, 5) * 1000 + R.randint(1, 19) * 50
        if R.random() < .5:
            s = a + b
            w = ["%d 公里 %d 公尺" % (a // 1000 + b // 1000, a % 1000 + b % 1000), K(s + 1000), K(s - 1000), K(s + 100)]
            return mcq("%s ＋ %s ＝" % (K(a), K(b)), K(s), w, "公里加公里、公尺加公尺，滿 1000 公尺換成 1 公里：%s。" % K(s))
        if a <= b:
            return None
        d = a - b
        if d % 1000 == 0:
            return None
        w = ["%d 公里 %d 公尺" % (a // 1000 - b // 1000, abs(a % 1000 - b % 1000)) if a % 1000 != b % 1000 else K(d + 100), K(d + 1000), K(d + 100), K(d - 100)]
        return mcq("%s － %s ＝" % (K(a), K(b)), K(d), w, "公尺不夠減，向公里借 1 公里 ＝ 1000 公尺：%s。" % K(d))
    return pick_unique(R, cmp_, 8, seen) + pick_unique(R, add, 12, seen)


def s5(seen):
    def trip():
        a, b = R.randint(1, 8) * 1000 + R.randint(1, 9) * 100, R.randint(1, 6) * 1000 + R.randint(1, 9) * 100
        who = NM.next()
        q = "%s騎腳踏車，上午騎了 %s，下午騎了 %s。一共騎了多遠？" % (who, K(a), K(b))
        s = a + b
        return mcq(q, K(s), ["%d 公里 %d 公尺" % (a // 1000 + b // 1000, a % 1000 + b % 1000) if a % 1000 + b % 1000 >= 1000 else K(s + 1000), K(abs(a - b)), K(s - 1000), K(s + 100)],
                   "%s ＋ %s ＝ %s。" % (K(a), K(b), K(s)))

    def left():
        tot = R.randint(3, 12) * 1000
        gone = R.randint(1, tot // 1000 - 1) * 1000 + R.randint(1, 9) * 100
        q = "從家到外婆家有 %d 公里，已經走了 %s，還要走多遠？" % (tot // 1000, K(gone))
        d = tot - gone
        return mcq(q, K(d), [K(d + 1000), "%d 公里 %d 公尺" % (tot // 1000 - gone // 1000, gone % 1000), K(tot + gone), K(d - 100)],
                   "%d 公里 ＝ %s 公尺，%s － %s ＝ %s 公尺 ＝ %s。" % (tot // 1000, num(tot), num(tot), num(gone), num(d), K(d)))

    def daily():
        per = R.randint(3, 9) * 100 + R.choice([0, 50])
        n = R.randint(5, 20)
        q = "%s每天走路上學，來回一共 %d 公尺。%d 天一共走了多遠？" % (NM.next(), per, n)
        v = per * n
        return mcq(q, K(v), [K(v + per), K(v - per), "%d 公里" % (v // 100), K(v + 1000)], "%d × %d ＝ %s 公尺 ＝ %s。" % (per, n, num(v), K(v)))
    return pick_unique(R, trip, 7, seen) + pick_unique(R, left, 7, seen) + pick_unique(R, daily, 6, seen)


def main():
    seen = set()
    sets = [("公里的量感", s1(seen)), ("公里和公尺的換算", s2(seen)), ("其他長度單位的換算", s3(seen)),
            ("比長短和加減", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>1 公里 ＝ 1000 公尺</b>。走路大約 15 分鐘可以走 1 公里。",
         "2 公里 50 公尺 ＝ 2000 ＋ 50 ＝ 2050 公尺。換算時公尺寫成 4 位數，不夠的位補 0。",
         "長度單位：1 公里 ＝ 1000 公尺，1 公尺 ＝ 100 公分，1 公分 ＝ 10 毫米。"],
        [example("3 公里 600 公尺 ＋ 1 公里 700 公尺 ＝", ["公尺：600 ＋ 700 ＝ 1300 ＝ 1 公里 300 公尺。", "公里：3 ＋ 1 ＋ 1 ＝ 5。"], "5 公里 300 公尺"),
         example("操場一圈 400 公尺，跑 3 公里要幾圈？", ["3 公里 ＝ 3000 公尺。", "3000 ÷ 400 ＝ 7……200，再跑半圈。"], "7 圈半")],
        [("2 公里 50 公尺 ＝ 250 公尺", "2 公里是 2000 公尺：2050 公尺"),
         ("1 公里 ＝ 100 公尺", "1 公里 ＝ 1000 公尺"),
         ("答案寫成 4 公里 1300 公尺", "滿 1000 公尺要換成 1 公里")])
    faq = [{"q": "1 公里等於幾公尺？",
            "a": "1 公里 ＝ 1000 公尺。學校操場一圈常見 200 公尺或 400 公尺，走路大約 15 分鐘可以走 1 公里。"},
           {"q": "四年級的長度單元要學什麼？",
            "a": "108課綱 N-4-9：認識公里，用生活中的例子做應用，並做公里、公尺、公分、毫米之間的換算和計算。"},
           {"q": "怎麼讓孩子對 1 公里有感覺？",
            "a": "帶孩子走一段 1 公里的路（例如操場 400 公尺跑 2 圈半），記下大約要走多久，之後就能用時間來估距離。"}]
    make_unit(R, "grade-4", "kilometers", "N-4-9",
              "長度：「公里」。生活實例之應用。含其他長度單位的換算與計算。",
              "長度：公里和公尺",
              "四年級數學 公里 練習題｜公里和公尺換算・長度單位・路程 學習單（附解答）",
              "公里和公尺",
              "國小四年級數學「公里」免費學習單：公里的量感、1公里＝1000公尺的換算、公尺公分毫米的換算、比長短和加減與路程應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 公里 ＝ 1000 公尺",
              "滿 1000 公尺換成 1 公里；換算時公尺寫成 4 位數。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
