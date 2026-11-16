# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：同分母分數（真分數、假分數、帶分數）（108課綱 N-4-5）
  python3 tools/gen_tw_math_g4_fractions.py
名前（真・假・帶分數）、假分數⇔帶分數、同分母の比較、加減（帶分數を含む）、整數倍、應用問題。
誤答：分母同士も足す、帶分數→假分數で整數×分母を忘れる（2又3/5→5/5）、借りるとき 10 を借りる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, mx

R = random.Random(41006)
NM = Names(R)


def show(n, d):
    """假分數のまま"""
    return fr(n, d)


def as_mixed(n, d):
    w, r = divmod(n, d)
    if r == 0:
        return str(w)
    return mx(w, r, d)


def s1(seen):
    def kind():
        d = R.randint(3, 12)
        t = R.choice(["真", "假", "帶"])
        if t == "真":
            v = fr(R.randint(1, d - 1), d)
        elif t == "假":
            v = fr(R.randint(d, 3 * d), d)
        else:
            v = mx(R.randint(1, 5), R.randint(1, d - 1), d)
        ans = t + "分數"
        return mcq("%s 是什麼分數？" % v, ans, [x + "分數" for x in "真假帶" if x != t] + ["整數"],
                   {"真": "分子比分母小，是真分數（比 1 小）。", "假": "分子大於或等於分母，是假分數（等於或大於 1）。",
                    "帶": "由整數和真分數合起來，是帶分數。"}[t])

    def to_mixed():
        d = R.randint(3, 9)
        n = R.randint(d + 1, 5 * d)
        if n % d == 0:
            return None
        w, r = divmod(n, d)
        return mcq("把 %s 化成帶分數。" % show(n, d), mx(w, r, d), [mx(w, d - r, d) if d - r != r else mx(w + 1, r, d), mx(r, w, d) if w < d and r != w else mx(w - 1 if w > 1 else w + 1, r, d), mx(w + 1, r, d), fr(r, d)],
                   "%d ÷ %d ＝ %d……%d，整數是 %d，剩下 %s：%s。" % (n, d, w, r, w, fr(r, d), mx(w, r, d)))

    def to_improper():
        d = R.randint(3, 9)
        w, r = R.randint(1, 6), R.randint(1, d - 1)
        n = w * d + r
        return mcq("把 %s 化成假分數。" % mx(w, r, d), show(n, d), [show(w + r, d), show(w * r + d, d) if w * r + d != n else show(n + 1, d), show(n + d, d), show(w * 10 + r, d) if w * 10 + r != n else show(n - 1, d)],
                   "%d ＝ %s，再加 %s：%s。（整數 × 分母 ＋ 分子）" % (w, show(w * d, d), fr(r, d), show(n, d)))
    return pick_unique(R, kind, 6, seen) + pick_unique(R, to_mixed, 7, seen) + pick_unique(R, to_improper, 7, seen)


def s2(seen):
    def cmp_():
        d = R.randint(3, 10)
        a = R.randint(d + 1, 4 * d)
        w, r = R.randint(1, 4), R.randint(1, d - 1)
        b = w * d + r
        if a == b or a % d == 0:
            return None
        sign = ">" if a > b else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % (show(a, d), mx(w, r, d)), sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "%s ＝ %s，分母一樣，比分子：%d %s %d。" % (mx(w, r, d), show(b, d), a, sign, b))

    def big():
        d = R.randint(4, 9)
        ns = R.sample(range(1, 4 * d), 4)
        if any(n % d == 0 for n in ns):
            return None
        labs = [show(n, d) if i % 2 == 0 else as_mixed(n, d) for i, n in enumerate(ns)]
        ans = labs[ns.index(max(ns))]
        return mcq("哪一個最大？%s" % "、".join(labs), ans, [l for l in labs if l != ans], "都化成假分數比分子：最大的是 %s。" % show(max(ns), d))
    return pick_unique(R, cmp_, 12, seen) + pick_unique(R, big, 8, seen)


def s3(seen):
    def add():
        d = R.randint(4, 12)
        a, b = R.randint(1, d - 1), R.randint(1, d - 1)
        s = a + b
        if R.random() < .5:
            q = "%s ＋ %s ＝" % (fr(a, d), fr(b, d))
            return mcq(q, as_mixed(s, d) if s != d else "1", [fr(s, 2 * d), fr(s, d) if s > d else fr(s + 1, d), as_mixed(s + 1, d), fr(a * b, d) if a * b != s else fr(s + 2, d)],
                       "分母不變，分子相加：%d ＋ %d ＝ %d，是 %s%s。" % (a, b, s, show(s, d), "" if s < d else " ＝ " + as_mixed(s, d)))
        w1, w2 = R.randint(1, 5), R.randint(1, 4)
        q = "%s ＋ %s ＝" % (mx(w1, a, d), mx(w2, b, d))
        tot = (w1 + w2) * d + s
        return mcq(q, as_mixed(tot, d), ["%d%s" % (w1 + w2, fr(s, d)) if s > d else as_mixed(tot + d, d), as_mixed(tot - d, d), mx(w1 + w2, s, 2 * d) if s < 2 * d else as_mixed(tot + 1, d), as_mixed(tot + 1, d)],
                   "整數加整數，分數加分數：%d ＋ %d ＝ %d，%s；%s。" % (w1, w2, w1 + w2, "%s ＋ %s ＝ %s" % (fr(a, d), fr(b, d), as_mixed(s, d)), "答案 " + as_mixed(tot, d)))
    return pick_unique(R, add, 20, seen)


def s4(seen):
    def sub():
        d = R.randint(4, 12)
        w1 = R.randint(2, 7)
        a, b = R.randint(1, d - 1), R.randint(1, d - 1)
        w2 = R.randint(0, w1 - 1)
        A = w1 * d + a
        B = w2 * d + b
        if A <= B:
            return None
        diff = A - B
        q = "%s － %s ＝" % (mx(w1, a, d), mx(w2, b, d) if w2 else fr(b, d))
        w = [mx(w1 - w2, abs(a - b), d) if a < b and abs(a - b) else as_mixed(diff + d, d),
             mx(w1 - w2 - 1, a + 10 - b, d) if a < b and a + 10 - b < d and w1 - w2 - 1 > 0 else as_mixed(diff - 1, d) if diff > 1 else as_mixed(diff + 2, d),
             as_mixed(diff + 1, d), as_mixed(diff - d, d) if diff > d else as_mixed(diff + 2 * d, d)]
        return mcq(q, as_mixed(diff, d), w,
                   ("分數不夠減，從整數借 1 ＝ %s：" % show(d, d) if a < b else "整數減整數，分數減分數：") + "%s － %s ＝ %s。" % (mx(w1, a, d), mx(w2, b, d) if w2 else fr(b, d), as_mixed(diff, d)))

    def from1():
        d = R.randint(3, 12)
        w = R.randint(1, 6)
        b = R.randint(1, d - 1)
        q = "%d － %s ＝" % (w, fr(b, d))
        diff = w * d - b
        return mcq(q, as_mixed(diff, d), [mx(w - 1, b, d) if w > 1 else fr(b, d) if False else mx(w, b, d), as_mixed(diff + d, d), fr(d - b, d) if w > 1 else fr(b + 1, d) if b + 1 < d else fr(1, d), mx(w - 1, d - b, d * 10) if w > 1 else as_mixed(diff + 1, d)],
                   "把 1 看成 %s：%d ＝ %s，%s － %s ＝ %s。" % (show(d, d), w, mx(w - 1, d, d) if w > 1 else show(d, d), mx(w - 1, d, d) if w > 1 else show(d, d), fr(b, d), as_mixed(diff, d)))

    def times():
        d = R.randint(3, 10)
        a = R.randint(1, d - 1)
        k = R.randint(2, 9)
        q = "%s × %d ＝" % (fr(a, d), k)
        v = a * k
        return mcq(q, as_mixed(v, d), [fr(a * k, d * k), as_mixed(v + a, d), fr(a, d * k), as_mixed(v - 1, d) if v > 1 else fr(2, d)],
                   "%d 個 %s：分子 %d × %d ＝ %d，%s ＝ %s。分母不變。" % (k, fr(a, d), a, k, v, show(v, d), as_mixed(v, d)))
    return pick_unique(R, sub, 8, seen) + pick_unique(R, from1, 5, seen) + pick_unique(R, times, 7, seen)


def s5(seen):
    def ribbon():
        d = R.choice([4, 5, 8, 10])
        w1, a = R.randint(2, 6), R.randint(1, d - 1)
        b = R.randint(1, d - 1)
        if a == b:
            return None
        who = NM.next()
        q = "%s有 %s 公尺的緞帶，用掉 %s 公尺，還剩幾公尺？" % (who, mx(w1, a, d), fr(b, d))
        diff = w1 * d + a - b
        return mcq(q, as_mixed(diff, d) + " 公尺", [as_mixed(w1 * d + a + b, d) + " 公尺", as_mixed(diff + d, d) + " 公尺", as_mixed(diff + 1, d) + " 公尺", as_mixed(diff - 1, d) + " 公尺"],
                   "%s － %s ＝ %s（公尺）。" % (mx(w1, a, d), fr(b, d), as_mixed(diff, d)))

    def cups():
        d = R.choice([3, 4, 5, 6, 8])
        a = R.randint(1, d - 1)
        k = R.randint(3, 9)
        q = "每杯果汁有 %s 公升，%d 杯一共有幾公升？" % (fr(a, d), k)
        v = a * k
        return mcq(q, as_mixed(v, d) + " 公升", [fr(v, d * k) + " 公升", as_mixed(v + a, d) + " 公升", as_mixed(v + d, d) + " 公升", fr(a + k, d) + " 公升" if a + k != v else as_mixed(v + 2, d) + " 公升"],
                   "%s × %d ＝ %s ＝ %s（公升）。" % (fr(a, d), k, show(v, d), as_mixed(v, d)))

    def run():
        d = R.choice([4, 5, 10])
        a, b = R.randint(1, d - 1), R.randint(1, d - 1)
        w1, w2 = R.randint(1, 3), R.randint(1, 3)
        who = NM.next()
        q = "%s星期六跑了 %s 公里，星期日跑了 %s 公里，兩天一共跑了幾公里？" % (who, mx(w1, a, d), mx(w2, b, d))
        tot = (w1 + w2) * d + a + b
        return mcq(q, as_mixed(tot, d) + " 公里", ["%d%s 公里" % (w1 + w2, fr(a + b, d)) if a + b > d else as_mixed(tot + d, d) + " 公里", as_mixed(tot - d, d) + " 公里", mx(w1 + w2, a + b, 2 * d) + " 公里" if a + b < 2 * d else as_mixed(tot + 1, d) + " 公里", as_mixed(tot + 1, d) + " 公里"],
                   "%s ＋ %s ＝ %s（公里）。" % (mx(w1, a, d), mx(w2, b, d), as_mixed(tot, d)))
    return pick_unique(R, ribbon, 7, seen) + pick_unique(R, cups, 7, seen) + pick_unique(R, run, 6, seen)


def main():
    seen = set()
    sets = [("真分數、假分數、帶分數", s1(seen)), ("比大小", s2(seen)), ("同分母分數的加法", s3(seen)),
            ("減法和整數倍", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>真分數</b>：分子比分母小（%s）。<b>假分數</b>：分子大於或等於分母（%s）。<b>帶分數</b>：整數和真分數合起來（%s）。" % (fr(3, 5), fr(7, 5), mx(1, 2, 5)),
         "假分數 → 帶分數：分子 ÷ 分母，商是整數，餘數是分子。帶分數 → 假分數：<b>整數 × 分母 ＋ 分子</b>。",
         "同分母分數相加減：<b>分母不變</b>，分子相加減。整數倍：分子乘以整數。"],
        [example("%s 化成帶分數" % fr(17, 5), ["17 ÷ 5 ＝ 3……2。"], mx(3, 2, 5)),
         example("%s － %s ＝" % (mx(3, 1, 5), fr(3, 5)), ["%s 不夠減 %s，從 3 借 1：%s。" % (fr(1, 5), fr(3, 5), mx(2, 6, 5)), "%s － %s ＝ %s。" % (mx(2, 6, 5), fr(3, 5), mx(2, 3, 5))], mx(2, 3, 5))],
        [("%s ＋ %s ＝ %s" % (fr(2, 5), fr(1, 5), fr(3, 10)), "分母不變：%s" % fr(3, 5)),
         ("%s ＝ %s" % (mx(2, 3, 5), fr(5, 5)), "整數 × 分母 ＋ 分子：2 × 5 ＋ 3 ＝ 13，是 %s" % fr(13, 5)),
         ("借 1 的時候當成借 10", "借的 1 是 %s，不是 10" % fr(5, 5))])
    faq = [{"q": "真分數、假分數、帶分數有什麼不同？",
            "a": "真分數比 1 小（分子比分母小）；假分數等於或大於 1（分子大於或等於分母）；帶分數是整數加上一個真分數，例如 2又3/5。"},
           {"q": "帶分數怎麼化成假分數？",
            "a": "整數 × 分母 ＋ 分子 當新的分子，分母不變。例如 2又3/5：2 × 5 ＋ 3 ＝ 13，是 13/5。"},
           {"q": "四年級的分數要學什麼？",
            "a": "108課綱 N-4-5：認識真分數、假分數、帶分數，會互相變換，並做同分母分數的比較、加、減與整數倍。"}]
    make_unit(R, "grade-4", "fractions", "N-4-5",
              "同分母分數：一般同分母分數教學（包括「真分數」、「假分數」、「帶分數」名詞引入）。假分數和帶分數之變換。同分母分數的比較、加、減與整數倍。",
              "同分母分數：真分數、假分數、帶分數",
              "四年級數學 分數 練習題｜假分數・帶分數・同分母分數加減 學習單（附解答）",
              "假分數和帶分數",
              "國小四年級數學「同分母分數」免費學習單：真分數、假分數、帶分數，假分數和帶分數的變換，比大小，同分母分數的加減和整數倍與應用題。100題線上練習馬上對答案，附可列印解答。",
              "帶分數 → 假分數：整數 × 分母 ＋ 分子",
              "同分母分數相加減，分母不變，分子相加減。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
