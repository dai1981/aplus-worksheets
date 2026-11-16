# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：長度「毫米」（108課綱 N-3-12）
  python3 tools/gen_tw_math_g3_millimeters.py
尺の報讀（公分・毫米）、1 公分＝10 毫米の換算、比大小、公分・毫米の加減、量感（適當的單位）と應用問題。
誤答：3公分6毫米→306毫米、48毫米→48公分、繰り上がりを忘れる（5公分13毫米）、0から量っていない。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, GREEN, FILL, INK

R = random.Random(31012)
NM = Names(R)
PX = 6          # 1 毫米 = 6px


def cm_mm(mm):
    c, m = divmod(mm, 10)
    if c and m:
        return "%d 公分 %d 毫米" % (c, m)
    if c:
        return "%d 公分" % c
    return "%d 毫米" % m


def ruler(start_mm, length_mm, cm=8):
    w = cm * 10 * PX + 40
    x0 = 20
    s = ["<rect x='%d' y='40' width='%d' height='46' fill='#fffbe6' stroke='%s' stroke-width='1.5'/>" % (x0 - 10, cm * 10 * PX + 20, INK)]
    for i in range(cm * 10 + 1):
        x = x0 + i * PX
        h = 22 if i % 10 == 0 else (15 if i % 5 == 0 else 9)
        s.append(line(x, 40, x, 40 + h, INK, 1.5 if i % 10 == 0 else 1))
        if i % 10 == 0:
            s.append(text(x, 80, str(i // 10), 13))
    s.append("<rect x='%d' y='12' width='%d' height='22' rx='3' fill='%s' stroke='%s' stroke-width='2'/>" % (
        x0 + start_mm * PX, length_mm * PX, FILL, GREEN))
    s.append(line(x0 + start_mm * PX, 12, x0 + start_mm * PX, 44, GREEN, 1.5, " stroke-dasharray='3 2'"))
    s.append(line(x0 + (start_mm + length_mm) * PX, 12, x0 + (start_mm + length_mm) * PX, 44, GREEN, 1.5, " stroke-dasharray='3 2'"))
    s.append(text(w - 18, 100, "公分", 12, anchor="end"))
    return fig(svg_wrap(w, 104, "".join(s), "尺上量長條的長度"))


def s1(seen):
    def mk():
        start = 0 if R.random() < .6 else R.randint(1, 2) * 10
        L = R.randint(12, 79 - start)
        if L % 10 == 0:
            return None
        q = "長條有多長？" + ruler(start, L)
        w = [cm_mm(L + start), cm_mm(L + 1), cm_mm(L - 1), cm_mm(L + 10), "%d 公分" % L]
        return mcq(q, cm_mm(L), w,
                   "%s長條 %s：大格是公分，小格是毫米。" % ("從 %d 公分量到 %s，要相減。" % (start // 10, cm_mm(start + L)) if start else "從 0 量起，", cm_mm(L)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def to_mm():
        c, m = R.randint(1, 15), R.randint(1, 9)
        q = "%d 公分 %d 毫米 ＝ ___ 毫米" % (c, m)
        a = c * 10 + m
        return mcq(q, str(a), [str(x) for x in (int("%d0%d" % (c, m)), c + m, c * 100 + m, a + 10)],
                   "1 公分 ＝ 10 毫米，%d 公分 ＝ %d 毫米，再加 %d 毫米 ＝ %d 毫米。" % (c, c * 10, m, a))

    def to_cm():
        a = R.randint(11, 159)
        if a % 10 == 0:
            return None
        c, m = divmod(a, 10)
        q = "%d 毫米 ＝ ___ 公分 ___ 毫米" % a
        return mcq(q, "%d 公分 %d 毫米" % (c, m),
                   ["%d 公分 %d 毫米" % x for x in ((m, c) if m != c and c < 10 else (c + 1, m), (c // 10 or c + 2, a % 100 if a >= 100 else m + 1), (c - 1, m + 10 if m < 10 else m), (c + 1, m))],
                   "每 10 毫米是 1 公分：%d ÷ 10 ＝ %d……%d，所以是 %d 公分 %d 毫米。" % (a, c, m, c, m))

    def whole():
        c = R.randint(2, 30)
        if R.random() < .5:
            q = "%d 公分 ＝ ___ 毫米" % c
            return mcq(q, str(c * 10), [str(x) for x in (c, c * 100, c + 10, c * 10 + 10)], "1 公分 ＝ 10 毫米，%d 公分 ＝ %d 毫米。" % (c, c * 10))
        q = "%d 毫米 ＝ ___ 公分" % (c * 10)
        return mcq(q, str(c), [str(x) for x in (c * 10, c * 100, c + 10, c * 10 // 100 if c >= 10 else c + 1)],
                   "10 毫米 ＝ 1 公分，%d 毫米 ＝ %d 公分。" % (c * 10, c))
    return pick_unique(R, to_mm, 8, seen) + pick_unique(R, to_cm, 7, seen) + pick_unique(R, whole, 5, seen)


def s3(seen):
    def mk():
        a = R.randint(21, 99)
        b = a + R.choice([-9, -6, -3, -1, 1, 4, 8])
        if a % 10 == 0 or b % 10 == 0 or b <= 10:
            return None
        c, m = divmod(a, 10)
        q = "%d 公分 %d 毫米 ○ %d 毫米，○ 裡要填什麼？" % (c, m, b)
        sign = ">" if a > b else "<"
        return mcq(q, sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "%d 公分 %d 毫米 ＝ %d 毫米，%d %s %d。" % (c, m, a, a, sign, b))

    def longest():
        xs = R.sample(range(21, 99), 4)
        if any(x % 10 == 0 for x in xs):
            return None
        big = max(xs)
        lab = []
        for i, x in enumerate(xs):
            lab.append(cm_mm(x) if i % 2 == 0 else "%d 毫米" % x)
        q = "哪一個最長？%s" % "、".join(lab)
        ans = lab[xs.index(big)]
        return mcq(q, ans, [l for l in lab if l != ans], "都換成毫米再比：最長的是 %d 毫米。" % big)
    return pick_unique(R, mk, 12, seen) + pick_unique(R, longest, 8, seen)


def s4(seen):
    def add():
        a, b = R.randint(12, 69), R.randint(12, 49)
        if a % 10 == 0 or b % 10 == 0 or (a % 10 + b % 10 < 10 and R.random() < .6):
            return None
        s = a + b
        q = "%s ＋ %s ＝" % (cm_mm(a), cm_mm(b))
        w = ["%d 公分 %d 毫米" % (a // 10 + b // 10, a % 10 + b % 10), cm_mm(s + 10), cm_mm(s - 10), cm_mm(s + 1), "%d 毫米" % (s * 10)]
        return mcq(q, cm_mm(s), w, "公分加公分、毫米加毫米，毫米滿 10 換成 1 公分：%s。" % cm_mm(s))

    def sub():
        a = R.randint(30, 99)
        b = R.randint(11, a - 8)
        if a % 10 == 0 and R.random() < .6 or b % 10 == 0:
            return None
        d = a - b
        if d % 10 == 0:
            return None
        q = "%s － %s ＝" % (cm_mm(a), cm_mm(b))
        w = ["%d 公分 %d 毫米" % (a // 10 - b // 10, abs(a % 10 - b % 10)) if a % 10 != b % 10 else cm_mm(d + 20), cm_mm(d + 10), cm_mm(d - 10) if d > 10 else cm_mm(d + 20), cm_mm(d + 1), cm_mm(d - 1)]
        return mcq(q, cm_mm(d), w, "毫米不夠減，向公分借 1 公分 ＝ 10 毫米：%s。" % cm_mm(d))
    return pick_unique(R, add, 10, seen) + pick_unique(R, sub, 10, seen)


def s5(seen):
    ITEMS = [("一隻螞蟻的長度", "5", "毫米"), ("一枚 10 元硬幣的厚度", "2", "毫米"), ("一枝鉛筆的長度", "17", "公分"),
             ("一本數學課本的長度", "26", "公分"), ("教室門的高度", "2", "公尺"), ("一粒米的長度", "5", "毫米"),
             ("一張悠遊卡的長度", "86", "毫米"), ("從學校到火車站的距離", "3", "公里"), ("手指甲的寬度", "1", "公分"),
             ("一顆鈕扣的厚度", "3", "毫米")]

    def unit():
        it, n, u = R.choice(ITEMS)
        q = "%s大約是 %s 多少？" % (it, n)
        q = "%s大約是 %s ___，___ 裡填哪一個單位最合適？" % (it, n)
        return mcq(q, u, [x for x in ("毫米", "公分", "公尺", "公里") if x != u], "想一想實際的大小：%s大約是 %s %s。" % (it, n, u))

    def word():
        kind = R.choice(["tape", "grow", "two"])
        who = NM.next()
        if kind == "tape":
            a = R.randint(60, 150)
            b = R.randint(12, 45)
            if a % 10 == 0 or b % 10 == 0:
                return None
            q = "%s的緞帶長 %s，剪掉 %d 毫米，還剩多長？" % (who, cm_mm(a), b)
            d = a - b
            if d % 10 == 0:
                return None
            return mcq(q, cm_mm(d), [cm_mm(a + b), cm_mm(d + 10), cm_mm(d - 10), "%d 毫米" % (a - b // 10)],
                       "%s ＝ %d 毫米，%d － %d ＝ %d 毫米 ＝ %s。" % (cm_mm(a), a, a, b, d, cm_mm(d)))
        if kind == "grow":
            a = R.randint(31, 89)
            g = R.randint(4, 19)
            if a % 10 == 0 or (a + g) % 10 == 0:
                return None
            q = "一棵豆芽上星期高 %s，這星期長高了 %d 毫米。現在高多少？" % (cm_mm(a), g)
            return mcq(q, cm_mm(a + g), [cm_mm(a - g), cm_mm(a + g + 10), "%d 公分 %d 毫米" % (a // 10, a % 10 + g) if a % 10 + g >= 10 else cm_mm(a + g + 1), cm_mm(a + g - 10)],
                       "%d 毫米 ＋ %d 毫米 ＝ %d 毫米 ＝ %s。" % (a, g, a + g, cm_mm(a + g)))
        a, b = R.randint(41, 89), R.randint(21, 79)
        if a % 10 == 0 or b % 10 == 0 or a == b:
            return None
        q = "%s的鉛筆長 %s，橡皮擦長 %s。鉛筆比橡皮擦長多少？" % (who, cm_mm(max(a, b)), cm_mm(min(a, b)))
        d = abs(a - b)
        if d % 10 == 0:
            return None
        return mcq(q, cm_mm(d), [cm_mm(a + b), cm_mm(d + 10), cm_mm(d + 1), cm_mm(d - 1) if d > 1 else cm_mm(d + 2)],
                   "相差用減法：%s － %s ＝ %s。" % (cm_mm(max(a, b)), cm_mm(min(a, b)), cm_mm(d)))
    return pick_unique(R, unit, 8, seen) + pick_unique(R, word, 12, seen)


def main():
    seen = set()
    sets = [("用尺量公分和毫米", s1(seen)), ("公分和毫米的換算", s2(seen)), ("比長短", s3(seen)),
            ("公分和毫米的加減", s4(seen)), ("量感和應用問題", s5(seen))]
    demo = ruler(0, 36, 5)
    body = lesson(
        ["尺上 1 大格是 <b>1 公分</b>，1 公分平分成 10 小格，1 小格是 <b>1 毫米</b>。",
         "<b>1 公分 ＝ 10 毫米</b>。3 公分 6 毫米 ＝ 30 ＋ 6 ＝ 36 毫米。",
         "比長短、加減時，先換成同一個單位；毫米滿 10 就換成 1 公分。"],
        [example("長條有多長？" + demo, ["從 0 量起，3 大格是 3 公分。", "再數 6 小格是 6 毫米。"], "3 公分 6 毫米（36 毫米）"),
         example("4 公分 7 毫米 ＋ 2 公分 5 毫米 ＝", ["毫米：7 ＋ 5 ＝ 12，12 毫米 ＝ 1 公分 2 毫米。", "公分：4 ＋ 2 ＋ 1 ＝ 7。"], "7 公分 2 毫米")],
        [("3 公分 6 毫米 ＝ 306 毫米", "1 公分 ＝ 10 毫米：30 ＋ 6 ＝ 36 毫米"),
         ("答案寫成 6 公分 12 毫米", "毫米滿 10 要換成 1 公分：7 公分 2 毫米"),
         ("沒有從 0 開始量，就讀右邊的數", "要用右邊的刻度減左邊的刻度")])
    faq = [{"q": "1 公分等於幾毫米？",
            "a": "1 公分 ＝ 10 毫米。尺上 1 大格是 1 公分，裡面的 10 小格每格是 1 毫米。"},
           {"q": "三年級的「毫米」單元要學什麼？",
            "a": "108課綱 N-3-12：認識毫米，用尺實際測量、估測長度，做公分和毫米的換算與加減計算。"},
           {"q": "怎麼培養孩子的長度量感？",
            "a": "記住幾個生活中的例子：螞蟻大約 5 毫米、手指甲寬大約 1 公分、鉛筆大約 17 公分，估測時拿來比一比。"}]
    make_unit(R, "grade-3", "millimeters", "N-3-12",
              "長度：「毫米」。實測、量感、估測與計算。單位換算。",
              "長度：公分和毫米",
              "三年級數學 毫米 練習題｜公分和毫米換算・用尺測量・長度加減 學習單（附解答）",
              "公分和毫米",
              "國小三年級數學「毫米」免費學習單：用尺量公分和毫米、1公分＝10毫米的換算、比長短、長度加減與量感應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 公分 ＝ 10 毫米",
              "尺上 1 小格是 1 毫米；毫米滿 10 換成 1 公分。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
