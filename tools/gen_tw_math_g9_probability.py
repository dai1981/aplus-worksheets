# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：機率（108課綱 D-9-2、D-9-3）
  python3 tools/gen_tw_math_g9_probability.py
機率の意味（0〜1）、銅板・骰子・撲克牌・抽球の古典機率、二つの骰子の和（表）、樹狀圖（兩層・取回／不取回）、圖釘・筊杯など對稱でない物は實驗の相對次數で推估、餘事件。
誤答：二枚の銅板で「一正一反」を 1/3 とする、取り出しで分母を減らさない、約分しない、樣本空間を數え漏らす。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr, Names
from tw_g7 import tidy_sets

R = random.Random(81116)
NM = Names(R)


def P(f):
    f = F(f)
    if f == 0:
        return "0"
    if f == 1:
        return "1"
    return fr(f.numerator, f.denominator)


def s1(seen):
    FACTS = [("丟一枚公正的硬幣，出現正面的機率是？", P(F(1, 2)), [P(1), P(F(1, 3)), "0"], "只有正、反兩種，機會相等：1/2。"),
             ("丟兩枚公正的硬幣，出現「一正一反」的機率是？", P(F(1, 2)), [P(F(1, 3)), P(F(1, 4)), P(F(3, 4))], "所有情形：正正、正反、反正、反反共 4 種，一正一反有 2 種：2/4 ＝ 1/2。"),
             ("丟兩枚公正的硬幣，兩枚都是正面的機率是？", P(F(1, 4)), [P(F(1, 2)), P(F(1, 3)), P(F(3, 4))], "4 種情形中只有「正正」1 種：1/4。"),
             ("丟兩枚公正的硬幣，至少一枚正面的機率是？", P(F(3, 4)), [P(F(1, 2)), P(F(1, 4)), P(F(2, 3))], "1 － 兩枚都反面的機率 ＝ 1 － 1/4 ＝ 3/4。"),
             ("丟三枚公正的硬幣，三枚都是正面的機率是？", P(F(1, 8)), [P(F(1, 3)), P(F(1, 6)), P(F(3, 8))], "共 2 × 2 × 2 ＝ 8 種情形，正正正 1 種：1/8。"),
             ("丟三枚公正的硬幣，恰好兩枚正面的機率是？", P(F(3, 8)), [P(F(1, 4)), P(F(1, 2)), P(F(2, 3))], "8 種中正正反、正反正、反正正 3 種：3/8。"),
             ("一件事一定會發生，它的機率是？", "1", ["0", P(F(1, 2)), "100"], "必然發生的事件機率是 1。"),
             ("一件事不可能發生，它的機率是？", "0", ["1", P(F(1, 2)), "－1"], "不可能發生的事件機率是 0。"),
             ("下面哪一個不可能是一件事的機率？", P(F(5, 4)), ["0", P(F(3, 5)), "1"], "機率介於 0 和 1 之間，5/4 大於 1。"),
             ("某事件發生的機率是 0.3，它不發生的機率是？", "0.7", ["0.3", "0.6", "1.3"], "發生 ＋ 不發生 ＝ 1：1 － 0.3 ＝ 0.7。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def die():
        conds = [("出現偶數", [2, 4, 6]), ("出現奇數", [1, 3, 5]), ("點數大於 4", [5, 6]), ("點數小於 3", [1, 2]), ("出現 3 的倍數", [3, 6]),
                 ("點數是質數", [2, 3, 5]), ("點數至少 2", [2, 3, 4, 5, 6]), ("點數是 6 的因數", [1, 2, 3, 6]), ("出現 7 點", []), ("點數不大於 6", [1, 2, 3, 4, 5, 6])]
        c, xs = R.choice(conds)
        v = F(len(xs), 6)
        q = "丟一顆公正的骰子，%s的機率是？" % c
        w = [P(F(len(xs), 5)) if len(xs) <= 5 else P(F(5, 6)), P(F(len(xs) + 1, 6)) if len(xs) < 6 else P(F(1, 2)), P(1 - v) if 1 - v != v else P(F(1, 3))]
        return mcq(q, P(v), w, "共 6 種情形，符合的有 %s，共 %d 種：%s。" % ("、".join(map(str, xs)) if xs else "沒有", len(xs), P(v)))
    return out + pick_unique(R, die, 10, seen)


def s2(seen):
    def mk():
        t = R.choice(["sum", "same", "prod"])
        if t == "sum":
            s_ = R.randint(2, 12)
            n = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s_)
            q = "同時丟兩顆公正的骰子，點數和是 %d 的機率是？" % s_
            ex = "、".join("（%d，%d）" % (a, s_ - a) for a in range(1, 7) if 1 <= s_ - a <= 6)
            return mcq(q, P(F(n, 36)), [P(F(1, 11)), P(F(n, 21)) if F(n, 21) != F(n, 36) else P(F(1, 12)), P(F(n + 1, 36))], "共 6 × 6 ＝ 36 種，和是 %d 的有%s，共 %d 種：%s。" % (s_, ex, n, P(F(n, 36))))
        if t == "same":
            q = "同時丟兩顆公正的骰子，兩顆點數相同的機率是？"
            return mcq(q, P(F(1, 6)), [P(F(1, 36)), P(F(1, 12)), P(F(1, 3))], "共 36 種，相同的有（1，1）到（6，6）共 6 種：6/36 ＝ 1/6。")
        k = R.choice([6, 12, 4, 8, 10, 3])
        n = sum(1 for a in range(1, 7) for b in range(1, 7) if a * b == k)
        q = "同時丟兩顆公正的骰子，點數的積是 %d 的機率是？" % k
        ex = "、".join("（%d，%d）" % (a, k // a) for a in range(1, 7) if k % a == 0 and 1 <= k // a <= 6)
        return mcq(q, P(F(n, 36)), [P(F(n, 18)) if F(n, 18) != F(n, 36) else P(F(1, 9)), P(F(1, 6)) if F(1, 6) != F(n, 36) else P(F(1, 12)), P(F(n + 1, 36))], "共 36 種，積是 %d 的有%s，共 %d 種：%s。" % (k, ex, n, P(F(n, 36))))

    def diff():
        d = R.randint(0, 5)
        n = sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == d)
        q = "同時丟兩顆公正的骰子，點數差是 %d 的機率是？" % d
        return mcq(q, P(F(n, 36)), [P(F(n, 18)) if F(n, 18) != F(n, 36) else P(F(1, 9)), P(F(1, 6)) if F(1, 6) != F(n, 36) else P(F(1, 4)), P(F(n + 2, 36))], "共 36 種，點數差是 %d 的有 %d 種：%s。" % (d, n, P(F(n, 36))))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, diff, 6, seen)


def s3(seen):
    def card():
        conds = [("紅心", 13), ("紅色的牌", 26), ("A", 4), ("人頭牌（J、Q、K）", 12), ("黑桃 K", 1), ("數字是偶數的牌（2、4、6、8、10）", 20), ("黑色的人頭牌", 6), ("梅花或方塊", 26), ("不是紅心", 39), ("紅色的 A", 2)]
        c, n = R.choice(conds)
        q = "從一副 52 張的撲克牌（不含鬼牌）中任意抽一張，抽到「%s」的機率是？" % c
        return mcq(q, P(F(n, 52)), [P(F(n, 54)), P(F(1, n)) if n > 1 and F(1, n) != F(n, 52) else P(F(1, 4)), P(1 - F(n, 52)) if 1 - F(n, 52) != F(n, 52) else P(F(1, 4))], ("52 張中有 %d 張：%d/52 ＝ %s。" % (n, n, P(F(n, 52)))) if n > 1 else "52 張中只有 1 張：1/52。")

    def ball():
        r, w, b = R.randint(1, 8), R.randint(1, 8), R.randint(0, 6)
        T = r + w + b
        col, n = R.choice([("紅球", r), ("白球", w), ("不是紅球", w + b)] + ([("藍球", b)] if b else []))
        q = "袋中有紅球 %d 顆、白球 %d 顆%s，大小相同。任意取一顆，取到%s的機率是？" % (r, w, "、藍球 %d 顆" % b if b else "", col)
        return mcq(q, P(F(n, T)), [P(F(n, T - n)) if T - n and F(n, T - n) != F(n, T) else P(F(n, T + 1)), P(1 - F(n, T)) if 1 - F(n, T) != F(n, T) else P(F(1, T)), P(F(1, T)) if F(1, T) != F(n, T) else P(F(2, T + 1))], "共 %d 顆，%s %d 顆：%s。" % (T, col, n, P(F(n, T))))
    return pick_unique(R, card, 10, seen) + pick_unique(R, ball, 10, seen)


def s4(seen):
    def mk():
        r, w = R.randint(1, 6), R.randint(1, 6)
        T = r + w
        rep = R.random() < .5
        k = R.choice(["rr", "ww", "rw"])
        if rep:
            pr = F(r, T)
            pw = F(w, T)
            v = {"rr": pr * pr, "ww": pw * pw, "rw": 2 * pr * pw}[k]
            wrong = {"rr": F(r * (r - 1), T * (T - 1)) if r > 1 else F(1, T * T), "ww": F(w * (w - 1), T * (T - 1)) if w > 1 else F(1, T * T), "rw": pr * pw}[k]
        else:
            if (k == "rr" and r < 2) or (k == "ww" and w < 2):
                return None
            v = {"rr": F(r * (r - 1), T * (T - 1)), "ww": F(w * (w - 1), T * (T - 1)), "rw": F(2 * r * w, T * (T - 1))}[k]
            wrong = {"rr": F(r * r, T * T), "ww": F(w * w, T * T), "rw": F(r * w, T * (T - 1))}[k]
        nm = {"rr": "兩次都是紅球", "ww": "兩次都是白球", "rw": "一紅一白"}[k]
        q = "袋中有紅球 %d 顆、白球 %d 顆。%s取兩次，每次一顆，%s的機率是？（可以畫樹狀圖）" % (r, w, "取出後放回再" if rep else "取出後不放回，連續", nm)
        if rep:
            e = "放回：每次都是 %d 顆。%s。" % (T, {"rr": "%d/%d × %d/%d" % (r, T, r, T), "ww": "%d/%d × %d/%d" % (w, T, w, T), "rw": "紅白 ＋ 白紅 ＝ 2 × %d/%d × %d/%d" % (r, T, w, T)}[k])
        else:
            e = "不放回：第二次剩 %d 顆。%s。" % (T - 1, {"rr": "%d/%d × %d/%d" % (r, T, r - 1, T - 1), "ww": "%d/%d × %d/%d" % (w, T, w - 1, T - 1), "rw": "紅白 ＋ 白紅 ＝ %d/%d × %d/%d ＋ %d/%d × %d/%d" % (r, T, w, T - 1, w, T, r, T - 1)}[k])
        e += " ＝ %s" % P(v)
        return mcq(q, P(v), [P(wrong) if wrong != v else P(v / 2), P(F(1, 2)) if v != F(1, 2) else P(F(1, 3)), P(1 - v) if 1 - v != v else P(F(1, 4))], e.replace("。 ＝", " ＝") + "。")
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def pin():
        n = R.choice([100, 200, 500, 1000])
        up = R.randint(3, 7) * n // 10
        obj = R.choice(["圖釘", "瓶蓋"])
        q = "%s不是對稱的物體。丟 %d 次，有 %d 次針尖朝上。估計丟一次朝上的機率約是？" % (obj, n, up) if obj == "圖釘" else "%s不是對稱的物體。丟 %d 次，有 %d 次開口朝上。估計丟一次開口朝上的機率約是？" % (obj, n, up)
        v = F(up, n)
        return mcq(q, P(v), [P(F(1, 2)) if v != F(1, 2) else P(F(2, 5)), P(1 - v) if 1 - v != v else P(F(3, 5)), P(F(up, n + up))], "不對稱的物體不能假設機會相等，要用實驗的相對次數估計：%d ÷ %d ＝ %s。" % (up, n, P(v)))

    def bwei():
        n = R.choice([100, 200, 400])
        k = R.randint(4, 6) * n // 10
        q = "擲筊（一對筊杯）%d 次，其中「聖筊」（一正一反）出現 %d 次。依實驗估計，擲一次得到聖筊的機率約是？" % (n, k)
        v = F(k, n)
        return mcq(q, P(v), [P(F(1, 3)), P(F(1, 4)), P(1 - v) if 1 - v != v else P(F(2, 3))], "筊杯兩面形狀不同，不是對稱的物體，要用實驗結果估計：%d ÷ %d ＝ %s。" % (k, n, P(v)))

    def comp():
        p = R.choice([F(1, 5), F(2, 7), F(3, 8), F(1, 6), F(5, 12), F(3, 10), F(4, 9)])
        who = NM.next()
        q = "%s投籃命中的機率是 %s，投一次沒有命中的機率是？" % (who, P(p))
        return mcq(q, P(1 - p), [P(p), P(F(1, 2)) if 1 - p != F(1, 2) else P(F(1, 3)), P(F(p.denominator - p.numerator - 1, p.denominator)) if p.denominator - p.numerator - 1 > 0 else P(F(1, 4))], "命中 ＋ 沒命中 ＝ 1：1 － %s ＝ %s。" % (P(p), P(1 - p)))

    def expect():
        p = R.choice([F(1, 4), F(1, 5), F(2, 5), F(3, 10), F(1, 10)])
        n = R.choice([100, 200, 300, 500])
        q = "某遊戲中獎的機率是 %s，%d 人各玩一次，大約有幾人中獎？" % (P(p), n)
        v = int(p * n)
        return mcq(q, "%d 人" % v, ["%d 人" % x for x in (n - v, int(n * p * 2), v + 10)], "%d × %s ＝ %d（人）。機率表示大量重複時的比例，實際人數可能稍有不同。" % (n, P(p), v))
    return pick_unique(R, pin, 6, seen) + pick_unique(R, bwei, 4, seen) + pick_unique(R, comp, 5, seen) + pick_unique(R, expect, 5, seen)


def main():
    seen = set()
    sets = [("機率的意義與硬幣", s1(seen)), ("兩顆骰子", s2(seen)), ("撲克牌與抽球", s3(seen)),
            ("樹狀圖：兩次抽取", s4(seen)), ("實驗機率與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["每種結果出現機會相等時：<b>機率 ＝ 符合的情形數 ÷ 所有可能的情形數</b>。機率在 0 到 1 之間。",
         "兩步驟的事件可以用<b>樹狀圖</b>或表格列出所有情形，例如丟兩顆骰子有 6 × 6 ＝ 36 種。",
         "取出後<b>不放回</b>，第二次的總數要少 1。",
         "圖釘、筊杯等<b>不對稱</b>的物體，不能假設機會相等，要用大量實驗的相對次數來估計機率。",
         "某事件不發生的機率 ＝ 1 － 發生的機率。"],
        [example("丟兩枚硬幣，一正一反的機率", ["正正、正反、反正、反反。", "一正一反有 2 種。"], "<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>"),
         example("紅球 3、白球 2，不放回取兩次，都是紅球", ["<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span> × <span class='fr'><span class='fn'>2</span><span class='fd'>4</span></span>。"], "<span class='fr'><span class='fn'>3</span><span class='fd'>10</span></span>")],
        [("兩枚硬幣只有「兩正、兩反、一正一反」3 種，各 1/3", "一正一反有「正反」「反正」2 種，機率 1/2"),
         ("不放回時第二次還用原來的總數", "第二次總數要減 1"),
         ("圖釘針尖朝上的機率是 1/2", "不對稱，要做實驗估計")])
    faq = [{"q": "為什麼丟兩枚硬幣一正一反的機率不是 1/3？",
            "a": "把兩枚硬幣分成第一枚、第二枚，所有情形是正正、正反、反正、反反 4 種，機會相等；一正一反有 2 種，所以是 1/2。"},
           {"q": "實驗得到的機率和理論機率有什麼關係？",
            "a": "實驗次數越多，事件發生的相對次數會越接近理論機率；不對稱的物體沒有理論機率，就用實驗結果來估計。"},
           {"q": "九年級的機率要學什麼？",
            "a": "108課綱 D-9-2、D-9-3：機率的意義、兩層樹狀圖，具有對稱性情境（硬幣、骰子、撲克牌、抽球）的古典機率，以及不具對稱性物體（圖釘、圓錐、筊杯）的機率。"}]
    make_unit(R, "grade-9", "probability", "D-9-3",
              "古典機率：具有對稱性的情境下（銅板、骰子、撲克牌、抽球等）之機率；不具對稱性的物體（圖釘、圓錐、爻杯）。",
              "機率：硬幣、骰子與樹狀圖",
              "九年級數學 機率 練習題｜骰子・撲克牌・抽球・樹狀圖 學習單（附解答）",
              "機率",
              "國中九年級數學「機率：硬幣、骰子與樹狀圖」免費學習單：機率的意義、丟硬幣與兩顆骰子、撲克牌和抽球、用樹狀圖算放回與不放回、圖釘與擲筊的實驗機率。100題線上練習馬上對答案，附可列印解答。",
              "機率 ＝ 符合的情形數 ÷ 所有情形數",
              "不放回時第二次總數減 1；不對稱的物體用實驗估計。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
