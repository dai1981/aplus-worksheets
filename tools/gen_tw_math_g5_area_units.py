# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：面積單位「公畝」「公頃」「平方公里」（108課綱 N-5-12）
  python3 tools/gen_tw_math_g5_area_units.py
1 公畝＝100 平方公尺、1 公頃＝100 公畝＝10000 平方公尺、1 平方公里＝100 公頃。換算・量感・計算・概數。
誤答：1 公頃＝1000 平方公尺、1 平方公里＝1000 公頃（長さの 1000 倍と混同）、桁ずれ。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, dnum

R = random.Random(51013)
NM = Names(R)
U = [("公畝", "平方公尺", 100), ("公頃", "公畝", 100), ("公頃", "平方公尺", 10000), ("平方公里", "公頃", 100), ("平方公里", "平方公尺", 1000000)]


def s1(seen):
    def mk():
        big, small, f = R.choice(U)
        n = R.randint(2, 90)
        if R.random() < .5:
            return mcq("%d %s ＝ ___ %s" % (n, big, small), num(n * f), [num(n * f * 10), num(n * f // 10), num(n * 1000) if f != 1000 else num(n * 100)],
                       "1 %s ＝ %s %s，%d %s ＝ %s %s。" % (big, num(f), small, n, big, num(n * f), small))
        return mcq("%s %s ＝ ___ %s" % (num(n * f), small, big), str(n), [str(n * 10), num(n * f // 1000) if n * f // 1000 not in (n, n * 10, 0) else str(n * 100), dnum(n / 10, 1)],
                   "%s %s ＝ 1 %s，%s %s ＝ %d %s。" % (num(f), small, big, num(n * f), small, n, big))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        big, small, f = R.choice(U[:4])
        a, b = R.randint(1, 20), R.randint(1, f - 1)
        v = a * f + b
        q = "%d %s %d %s ＝ ___ %s" % (a, big, b, small, small)
        return mcq(q, num(v), [num(int("%d%d" % (a, b))), num(a * 1000 + b), num(v + f)], "%d %s ＝ %s %s，再加 %d：%s %s。" % (a, big, num(a * f), small, b, num(v), small))

    def dec():
        big, small, f = R.choice(U[:4])
        n = R.randint(11, 99) / 10
        v = int(round(n * f))
        q = "%s %s ＝ ___ %s" % (dnum(n, 1), big, small)
        return mcq(q, num(v), [num(v // 10), num(v * 10), dnum(n * 10, 0)], "%s × %s ＝ %s。" % (dnum(n, 1), num(f), num(v)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, dec, 8, seen)


def s3(seen):
    SENSE = [("一間教室的地板", "平方公尺"), ("一座學校操場", "公畝"), ("一個大公園", "公頃"), ("台北市的面積", "平方公里"),
             ("一張書桌的桌面", "平方公尺"), ("一塊小菜園", "平方公尺"), ("一座大農場", "公頃"), ("台灣的面積", "平方公里"),
             ("一個籃球場", "平方公尺"), ("一個小村子的稻田", "公頃")]
    out = []
    for it, u in SENSE:
        out.append(mcq("%s的面積，最適合用哪一個單位？" % it, u, [x for x in ("平方公尺", "公畝", "公頃", "平方公里") if x != u],
                       "想一想大小：%s用「%s」最合適。" % (it, u)))
    for o in out:
        seen.add(o["q"])

    def cmp_():
        big, small, f = R.choice(U[:4])
        a = R.randint(2, 30)
        b = a * f + R.choice([-f // 2, f // 10, -f // 10, f, f // 2])
        if b <= 0 or b == a * f:
            return None
        sign = ">" if a * f > b else "<"
        return mcq("%d %s ○ %s %s，○ 裡要填什麼？" % (a, big, num(b), small), sign, ["<" if sign == ">" else ">", "=", "無法比較"], "%d %s ＝ %s %s，%s %s %s。" % (a, big, num(a * f), small, num(a * f), sign, num(b)))
    return out + pick_unique(R, cmp_, 10, seen)


def s4(seen):
    def field():
        w, h = R.randint(10, 400) // 10 * 10, R.randint(10, 300) // 10 * 10
        w, h = max(w, h), min(w, h)
        A = w * h
        q = "一塊長 %d 公尺、寬 %d 公尺的長方形農地，面積是幾公畝？" % (w, h) if A % 100 == 0 and A < 100000 else None
        if not q:
            return None
        return mcq(q, "%s 公畝" % num(A // 100), ["%s 公畝" % num(x) for x in (A, A // 10, A // 1000 if A // 1000 else A * 10)], "%d × %d ＝ %s 平方公尺 ＝ %s 公畝。" % (w, h, num(A), num(A // 100)))

    def ha():
        w, h = R.randint(1, 9) * 100, R.randint(1, 9) * 100
        A = w * h
        q = "長 %d 公尺、寬 %d 公尺的長方形公園，面積是幾公頃？" % (w, h)
        return mcq(q, "%s 公頃" % num(A // 10000) if A % 10000 == 0 else "%s 公頃" % dnum(A / 10000, 2), ["%s 公頃" % x for x in (num(A // 100), dnum(A / 1000, 1), dnum(A / 100000, 3))],
                   "%d × %d ＝ %s 平方公尺，10000 平方公尺 ＝ 1 公頃，是 %s 公頃。" % (w, h, num(A), dnum(A / 10000, 2)))

    def km():
        w, h = R.randint(2, 30), R.randint(2, 20)
        q = "長 %d 公里、寬 %d 公里的長方形區域，面積是幾平方公里？是幾公頃？" % (w, h)
        A = w * h
        return mcq(q, "%d 平方公里，%s 公頃" % (A, num(A * 100)), ["%d 平方公里，%s 公頃" % (A, num(A * 1000)), "%d 平方公里，%s 公頃" % (2 * (w + h), num(2 * (w + h) * 100)), "%d 平方公里，%s 公頃" % (A, num(A * 10))],
                   "%d × %d ＝ %d 平方公里，1 平方公里 ＝ 100 公頃，%d × 100 ＝ %s 公頃。" % (w, h, A, A, num(A * 100)))
    return pick_unique(R, field, 7, seen) + pick_unique(R, ha, 7, seen) + pick_unique(R, km, 6, seen)


def s5(seen):
    def mk():
        kind = R.choice(["sell", "add", "rice"])
        if kind == "sell":
            a, b = R.randint(3, 20), R.randint(10, 90)
            q = "一塊 %d 公頃的土地，賣掉 %d 公畝，還剩多少公畝？" % (a, b)
            v = a * 100 - b
            return mcq(q, "%s 公畝" % num(v), ["%s 公畝" % num(x) for x in (a - b if a > b else a * 10 - b if a * 10 > b else a * 100 + b, a * 1000 - b, a * 100 + b)], "%d 公頃 ＝ %s 公畝，%s － %d ＝ %s（公畝）。" % (a, num(a * 100), num(a * 100), b, num(v)))
        if kind == "add":
            a, b = R.randint(20, 90), R.randint(20, 90)
            q = "%s家有兩塊稻田，一塊 %d 公畝、一塊 %d 公畝，合起來是幾公頃？" % (NM.next(), a, b)
            v = (a + b) / 100
            return mcq(q, "%s 公頃" % dnum(v, 2), ["%s 公頃" % x for x in (num(a + b), dnum((a + b) / 10, 1), dnum((a + b) / 1000, 3))], "%d ＋ %d ＝ %d 公畝 ＝ %s 公頃。" % (a, b, a + b, dnum(v, 2)))
        per = R.choice([5, 6, 7, 8])
        ha = R.randint(3, 30)
        q = "每公頃的稻田大約收成 %d 公噸稻米，%d 公頃大約收成幾公噸？" % (per, ha)
        return mcq(q, "%d 公噸" % (per * ha), ["%d 公噸" % x for x in (per * ha * 100, per + ha, per * ha * 10)], "%d × %d ＝ %d（公噸）。" % (per, ha, per * ha))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("面積單位的換算", s1(seen)), ("複名數和小數的換算", s2(seen)), ("量感和比大小", s3(seen)),
            ("算面積", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["邊長 10 公尺的正方形是 <b>1 公畝</b>（100 平方公尺）；邊長 100 公尺的正方形是 <b>1 公頃</b>（10,000 平方公尺）；邊長 1 公里的正方形是 <b>1 平方公里</b>。",
         "相鄰的單位都差 <b>100 倍</b>：1 公頃 ＝ 100 公畝，1 平方公里 ＝ 100 公頃。",
         "教室用平方公尺，操場用公畝，公園、農場用公頃，城市、國家用平方公里。"],
        [example("3 公頃 ＝ ___ 平方公尺", ["1 公頃 ＝ 10,000 平方公尺。", "3 × 10,000 ＝ 30,000。"], "30,000"),
         example("長 500 公尺、寬 200 公尺的公園是幾公頃？", ["500 × 200 ＝ 100,000 平方公尺。", "100,000 ÷ 10,000 ＝ 10。"], "10 公頃")],
        [("1 公頃 ＝ 1000 平方公尺", "1 公頃 ＝ 10,000 平方公尺（100 公尺 × 100 公尺）"),
         ("1 平方公里 ＝ 1000 公頃", "面積單位相差 100 倍：1 平方公里 ＝ 100 公頃"),
         ("把長度單位和面積單位混在一起", "1 公里 ＝ 1000 公尺，但 1 平方公里 ＝ 1,000,000 平方公尺")])
    faq = [{"q": "公畝、公頃、平方公里有多大？",
            "a": "1 公畝是邊長 10 公尺的正方形（100 平方公尺）；1 公頃是邊長 100 公尺的正方形（10,000 平方公尺）；1 平方公里是邊長 1 公里的正方形（100 公頃）。"},
           {"q": "1 公頃等於幾平方公尺？",
            "a": "1 公頃 ＝ 100 公畝 ＝ 10,000 平方公尺，大約是一個標準足球場再大一點。"},
           {"q": "五年級的面積單位要學什麼？",
            "a": "108課綱 N-5-12：認識公畝、公頃、平方公里，在生活中應用，並和平方公尺換算與計算，可以使用概數。"}]
    make_unit(R, "grade-5", "area-units", "N-5-12",
              "面積：「公畝」、「公頃」、「平方公里」。生活實例之應用。含與「平方公尺」的換算與計算。使用概數。",
              "面積單位：公畝、公頃、平方公里",
              "五年級數學 公畝公頃 練習題｜面積單位換算・平方公里 學習單（附解答）",
              "公畝、公頃、平方公里",
              "國小五年級數學「公畝、公頃、平方公里」免費學習單：面積單位的換算、複名數和小數、量感和比大小、算土地面積與應用題。100題線上練習馬上對答案，附可列印解答。",
              "相鄰的面積單位差 100 倍",
              "1 公頃 ＝ 10,000 平方公尺，1 平方公里 ＝ 100 公頃。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
