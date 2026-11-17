# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：加法直式（進位）（108課綱 N-2-2）
  python3 tools/gen_tw_math_g2_column_addition.py
二位數＋二位數（不進位・一次進位）、三位數＋二位數／三位數（一次進位）、直式を見て計算、位をそろえる、文章題。
誤答：進位の 1 を加え忘れる、位をそろえずに足す、繰り上がりを答えの左に書く（58 ＋ 7 ＝ 515）。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81302)
NM = Names(R)


def carries(a, b):
    c, n = 0, 0
    while a or b:
        if a % 10 + b % 10 + c >= 10:
            n += 1
            c = 1
        else:
            c = 0
        a //= 10
        b //= 10
    return n


def nocarry_sum(a, b):
    """進位を忘れた答え"""
    r, p = 0, 1
    while a or b:
        r += ((a % 10 + b % 10) % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def mk_add(lo1, hi1, lo2, hi2, need, show):
    def mk():
        a, b = R.randint(lo1, hi1), R.randint(lo2, hi2)
        if carries(a, b) != need or a + b > 999:
            return None
        s = a + b
        q = ("用直式算：" + P.col(a, b, "＋")) if show else "%d ＋ %d ＝ ？" % (a, b)
        w = [nocarry_sum(a, b) if need else s + 10, s + 10 if need else s + 1, s - 10 if s > 20 else s + 2, s + 1]
        return mcq(q, str(s), [str(x) for x in w if x != s][:3], ("個位對齊，從個位加起，滿十向前一位進 1：%d。" % s) if need else "個位加個位、十位加十位：%d。" % s)
    return mk


def s1(seen):
    return pick_unique(R, mk_add(10, 89, 10, 89, 0, False), 6, seen) + pick_unique(R, mk_add(10, 89, 10, 89, 1, True), 14, seen)


def s2(seen):
    return pick_unique(R, mk_add(10, 89, 10, 89, 1, False), 20, seen)


def s3(seen):
    return pick_unique(R, mk_add(100, 899, 10, 99, 1, True), 10, seen) + pick_unique(R, mk_add(100, 899, 10, 99, 1, False), 10, seen)


def s4(seen):
    return pick_unique(R, mk_add(100, 799, 100, 799, 1, True), 10, seen) + pick_unique(R, mk_add(100, 799, 100, 799, 1, False), 10, seen)


def s5(seen):
    def mk():
        a, b = R.randint(15, 600), R.randint(15, 300)
        if carries(a, b) != 1 or a + b > 999:
            return None
        who = NM.next()
        t = R.choice([("學校上午有 %d 人參觀，下午有 %d 人", "人", "一共有幾人參觀"), ("%s存了 %d 元，又存了 %d 元", "元", "現在一共有多少元"),
                      ("圖書館有 %d 本故事書和 %d 本漫畫", "本", "一共有幾本"), ("果園摘了 %d 顆橘子，又摘了 %d 顆", "顆", "一共摘了幾顆")])
        txt = t[0] % ((who, a, b) if t[0].startswith("%s") else (a, b))
        q = "%s。%s？" % (txt, t[2])
        s = a + b
        return mcq(q, "%d %s" % (s, t[1]), ["%d %s" % (x, t[1]) for x in (nocarry_sum(a, b), abs(a - b), s + 10)], "%d ＋ %d ＝ %d。" % (a, b, s))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("二位數加法直式", s1(seen)), ("二位數進位加法", s2(seen)), ("三位數加二位數", s3(seen)),
            ("三位數加三位數", s4(seen)), ("加法應用問題", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["直式要<b>個位對齊個位</b>，從個位開始加。" + P.col(258, 37, "＋"),
         "個位 8 ＋ 7 ＝ 15，寫 5，<b>滿十向十位進 1</b>；十位 5 ＋ 3 ＋ 1 ＝ 9；百位 2。",
         "答案 258 ＋ 37 ＝ 295。"],
        [example("46 ＋ 38", ["個位 6 ＋ 8 ＝ 14，寫 4 進 1。", "十位 4 ＋ 3 ＋ 1 ＝ 8。"], "84"),
         example("375 ＋ 152", ["個位 7、十位 7 ＋ 5 ＝ 12 寫 2 進 1。", "百位 3 ＋ 1 ＋ 1 ＝ 5。"], "527")],
        [("46 ＋ 38 ＝ 74", "進位的 1 要加上：84"),
         ("258 ＋ 37 時，37 和百位對齊", "個位對齊個位"),
         ("6 ＋ 8 ＝ 14，兩個數都寫下來", "只寫 4，1 進到十位")])
    faq = [{"q": "二年級的加法直式要學到哪裡？",
            "a": "108課綱 N-2-2：用位值理解多位數加減直式，處理一次進位和退位，三年級再學多次進位。"},
           {"q": "孩子常忘記進位怎麼辦？",
            "a": "要求孩子在十位上方寫一個小小的 1，算十位時一起加，養成習慣就不會忘。"},
           {"q": "為什麼一定要對齊？",
            "a": "直式是同一位相加，個位加個位、十位加十位，沒對齊就會把十位加到百位。"}]
    make_unit(R, "grade-2", "column-addition", "N-2-2",
              "加減算式與直式計算：用位值理解多位數加減計算。處理加數與被加數為二位數或三位數的計算。處理一次進、退位。",
              "加法直式：進位",
              "二年級數學 加法直式 練習題｜二位數三位數進位加法 學習單（附解答）",
              "加法直式",
              "國小二年級數學「加法直式：進位」免費學習單：二位數加法直式、進位加法、三位數加二位數和三位數、加法應用問題。100題線上練習，附可列印解答。",
              "個位對齊，滿十進一",
              "進位的 1 寫在上面，加下一位時一起加。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
