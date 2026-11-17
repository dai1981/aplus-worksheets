# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：減法直式（退位）（108課綱 N-2-2）
  python3 tools/gen_tw_math_g2_column_subtraction.py
二位數－二位數（不退位・一次退位）、三位數－二位數／三位數（一次退位）、驗算（差 ＋ 減數 ＝ 被減數）、文章題。
誤答：大きい方から小さい方を引く（52 － 37 で 7 － 2 ＝ 5 → 25）、借りた 1 を引き忘れる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81303)
NM = Names(R)


def borrows(a, b):
    c, n = 0, 0
    while a or b:
        if a % 10 - c < b % 10:
            n += 1
            c = 1
        else:
            c = 0
        a //= 10
        b //= 10
    return n


def bigsmall(a, b):
    """各位で大きい方から小さい方を引いた間違い"""
    r, p = 0, 1
    while a or b:
        r += abs(a % 10 - b % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def mk_sub(lo1, hi1, lo2, hi2, need, show, zero_mid=False):
    def mk():
        a, b = R.randint(lo1, hi1), R.randint(lo2, hi2)
        if a <= b or borrows(a, b) != need:
            return None
        if zero_mid and a // 10 % 10 != 0:
            return None
        d = a - b
        q = ("用直式算：" + P.col(a, b, "－")) if show else "%d － %d ＝ ？" % (a, b)
        w = [bigsmall(a, b) if need else d + 10, d + 10, d - 10 if d > 10 else d + 1, d + 1]
        return mcq(q, str(d), [str(x) for x in w if x != d][:3], ("哪一位不夠減，就向前一位借 1 當 10，前一位要少 1：%d。" % d) if need else "個位減個位、十位減十位：%d。" % d)
    return mk


def s1(seen):
    return pick_unique(R, mk_sub(20, 99, 10, 89, 0, False), 6, seen) + pick_unique(R, mk_sub(20, 99, 10, 89, 1, True), 14, seen)


def s2(seen):
    return pick_unique(R, mk_sub(20, 99, 10, 89, 1, False), 20, seen)


def s3(seen):
    return pick_unique(R, mk_sub(100, 999, 10, 99, 1, True), 10, seen) + pick_unique(R, mk_sub(100, 999, 10, 99, 1, False), 10, seen)


def s4(seen):
    def check():
        a, b = R.randint(200, 999), R.randint(100, 800)
        if a <= b or borrows(a, b) != 1:
            return None
        d = a - b
        q = "%d － %d ＝ %d，用哪一個算式驗算？" % (a, b, d)
        return mcq(q, "%d ＋ %d ＝ %d" % (d, b, a), ["%d ＋ %d ＝ %d" % (a, b, a + b), "%d － %d ＝ %d" % (a, d, b), "%d ＋ %d ＝ %d" % (d, a, d + a)], "驗算減法：差 ＋ 減數 ＝ 被減數。")
    return pick_unique(R, mk_sub(200, 999, 100, 899, 1, True), 8, seen) + pick_unique(R, mk_sub(200, 999, 100, 899, 1, False), 7, seen) + pick_unique(R, check, 5, seen)


def s5(seen):
    def mk():
        a, b = R.randint(40, 900), R.randint(15, 400)
        if a <= b or borrows(a, b) != 1:
            return None
        who = NM.next()
        t = R.choice([("%s有 %d 元，買書花了 %d 元", "元", "還剩多少元"), ("一本書有 %d 頁，%s看了 %d 頁", "頁", "還有幾頁沒看"),
                      ("學校有 %d 位學生，其中 %d 位是男生", "位", "女生有幾位"), ("哥哥跳了 %d 下，%s跳了 %d 下", "下", "哥哥多跳幾下")])
        if "頁" in t[1] and a > 300:
            return None
        if t[0].startswith("%s"):
            txt = t[0] % (who, a, b)
        elif "%s看" in t[0] or "%s跳" in t[0]:
            txt = t[0] % (a, who, b)
        else:
            txt = t[0] % (a, b)
        q = "%s。%s？" % (txt, t[2])
        d = a - b
        return mcq(q, "%d %s" % (d, t[1]), ["%d %s" % (x, t[1]) for x in (bigsmall(a, b), a + b, d + 10)], "%d － %d ＝ %d。" % (a, b, d))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("二位數減法直式", s1(seen)), ("二位數退位減法", s2(seen)), ("三位數減二位數", s3(seen)),
            ("三位數減三位數和驗算", s4(seen)), ("減法應用問題", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["直式要<b>個位對齊個位</b>，從個位開始減。" + P.col(352, 127, "－"),
         "個位 2 不夠減 7，<b>向十位借 1 當 10</b>：12 － 7 ＝ 5；十位剩 4，4 － 2 ＝ 2；百位 3 － 1 ＝ 2。",
         "<b>驗算</b>：差 ＋ 減數 ＝ 被減數，225 ＋ 127 ＝ 352。"],
        [example("52 － 37", ["個位 2 不夠減，借 1：12 － 7 ＝ 5。", "十位 4 － 3 ＝ 1。"], "15"),
         example("640 － 215", ["個位 0 不夠減，借 1：10 － 5 ＝ 5。", "十位 3 － 1 ＝ 2，百位 6 － 2 ＝ 4。"], "425")],
        [("52 － 37，個位用 7 － 2", "上面減下面，不夠減要借：12 － 7"),
         ("借了以後十位沒有少 1", "被借的那一位要減 1"),
         ("驗算用 被減數 ＋ 減數", "差 ＋ 減數 ＝ 被減數")])
    faq = [{"q": "退位減法最常錯在哪？",
            "a": "一是個位不夠減時直接用大的減小的，二是借了以後十位忘記少 1。可以在十位上劃掉、寫上新的數。"},
           {"q": "二年級的減法直式要學到哪裡？",
            "a": "108課綱 N-2-2：二位數、三位數的加減直式，處理一次退位；多次退位、跨 0 退位在三年級。"},
           {"q": "為什麼要驗算？",
            "a": "用加法檢查減法的答案，可以自己找出錯誤，養成檢查的習慣。"}]
    make_unit(R, "grade-2", "column-subtraction", "N-2-2",
              "加減算式與直式計算：用位值理解多位數加減計算。處理加數與被加數為二位數或三位數的計算。處理一次進、退位。",
              "減法直式：退位",
              "二年級數學 減法直式 練習題｜二位數三位數退位減法・驗算 學習單（附解答）",
              "減法直式",
              "國小二年級數學「減法直式：退位」免費學習單：二位數減法直式、退位減法、三位數減二位數和三位數、用加法驗算、減法應用問題。100題線上練習，附可列印解答。",
              "不夠減，向前一位借 1 當 10",
              "被借的那一位要少 1；差 ＋ 減數 ＝ 被減數。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
