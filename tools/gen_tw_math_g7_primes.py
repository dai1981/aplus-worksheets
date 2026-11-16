# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：100 以內的質數（108課綱 N-7-1）
  python3 tools/gen_tw_math_g7_primes.py
質數・合數の定義、質數の篩法（埃拉托斯特尼）、100 以內の判定（√n まで割る）、7・11 の倍數判別、應用（數字卡・連續整數）。
誤答：1 を質數とする、51・91・57 を質數とする、奇數はすべて質數とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets

R = random.Random(71009)
NM = Names(R)
PR = [p for p in range(2, 101) if all(p % d for d in range(2, int(p ** .5) + 1))]
TRAP = [51, 57, 87, 91, 93, 49, 77, 39, 69, 81, 63, 33, 27, 21, 99]


def least(n):
    for d in range(2, n):
        if n % d == 0:
            return d


def s1(seen):
    def mk():
        k = R.choice(["p", "c"])
        if k == "p":
            ans = R.choice([p for p in PR if p > 20])
            w = R.sample(TRAP, 3)
            return mcq("下面哪一個是<b>質數</b>？（%s）" % "、".join(map(str, sorted(w + [ans]))), str(ans), [str(x) for x in w], "%d 只有 1 和 %d 兩個因數。%s" % (ans, ans, "、".join("%d ＝ %d × %d" % (x, least(x), x // least(x)) for x in w[:2])) + "，都是合數。")
        ans = R.choice(TRAP)
        w = R.sample([p for p in PR if p > 20], 3)
        return mcq("下面哪一個是<b>合數</b>？（%s）" % "、".join(map(str, sorted(w + [ans]))), str(ans), [str(x) for x in w], "%d ＝ %d × %d，是合數；其他都是質數。" % (ans, least(ans), ans // least(ans)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    F_ = [("用篩法找 100 以內的質數，先劃掉 1，再把 2 留下、劃掉什麼？", "2 以外所有 2 的倍數", ["所有奇數", "所有 2 的因數", "2 和 4"], "篩法：留下質數本身，劃掉它的倍數。"),
          ("用篩法找 100 以內的質數，最少要篩到哪一個質數的倍數就夠了？", "7", ["5", "11", "97"], "因為 11 × 11 ＝ 121 ＞ 100，篩完 2、3、5、7 的倍數就夠了。"),
          ("100 以內的質數一共有幾個？", "25 個", ["24 個", "26 個", "50 個"], "100 以內有 25 個質數。"),
          ("1 到 50 有幾個質數？", "15 個", ["14 個", "16 個", "25 個"], "2、3、5、7、11、13、17、19、23、29、31、37、41、43、47，共 15 個。"),
          ("唯一的偶數質數是？", "2", ["0", "4", "沒有"], "2 只有因數 1 和 2；其他偶數都是 2 的倍數。"),
          ("質數的定義是什麼？", "大於 1，且只有 1 和本身兩個因數的整數", ["所有奇數", "不能被 2 整除的數", "只有一個因數的數"], "1 只有一個因數，不是質數。"),
          ("90 到 100 之間有幾個質數？", "1 個（97）", ["0 個", "2 個", "3 個"], "91 ＝ 7 × 13、93 ＝ 3 × 31、99 ＝ 9 × 11，只有 97 是質數。"),
          ("判斷 89 是不是質數，最多要試除到哪個質數？", "7", ["3", "11", "89"], "9 × 9 ＝ 81 ＜ 89 ＜ 100 ＝ 10 × 10，試 2、3、5、7 都除不盡，89 是質數。")]
    out = [mcq(*f) for f in F_]
    for o in out:
        seen.add(o["q"])

    def cnt():
        a = R.choice(range(10, 90, 10))
        b = a + 10
        ps = [p for p in PR if a < p < b]
        return mcq("%d 到 %d 之間有幾個質數？" % (a, b), "%d 個" % len(ps), ["%d 個" % x for x in (len(ps) + 1, len(ps) + 2, max(len(ps) - 1, 0) if len(ps) else 3)  if x != len(ps)] + ["5 個"], "有 %s。" % ("、".join(map(str, ps)) if ps else "沒有質數"))
    return out + pick_unique(R, cnt, 8, seen) + pick_unique(R, lambda: None or mk_trap(), 4, seen)


def mk_trap():
    n = R.choice(TRAP + [p for p in PR if p > 30])
    ok = n in PR
    return mcq("%d 是質數嗎？" % n, "是質數" if ok else "不是，%d ＝ %d × %d" % (n, least(n), n // least(n)), ["不是，因為它是奇數" if ok else "是質數", "不是，%d 是偶數" % n, "無法判斷"], ("%d 用 2、3、5、7 試除都除不盡，是質數。" % n) if ok else ("%d 可以被 %d 整除。" % (n, least(n))))


def s3(seen):
    def mk():
        n = R.randint(30, 100)
        if n % 2 == 0 or int(n ** .5) ** 2 == n:
            return None
        ps = [p for p in (2, 3, 5, 7) if p * p <= n]
        q = "判斷 %d 是不是質數：%d 介於 %d² 和 %d² 之間，至少要用哪些質數試除？" % (n, n, int(n ** .5), int(n ** .5) + 1)
        ans = "、".join(map(str, ps))
        return mcq(q, ans, ["、".join(map(str, ps[:-1])) if len(ps) > 1 else "2、3、5", "、".join(map(str, [p for p in PR if p < n][:len(ps) + 2])), "1 到 %d 的所有數" % n], "只要試到 √%d 以下的質數：%s。" % (n, ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def seven():
        n = R.randint(100, 999)
        p = R.choice([7, 11])
        if R.random() < .5:
            n = n - n % p
        if n < 100:
            return None
        ok = n % p == 0
        return mcq("%d 是不是 %d 的倍數？" % (n, p), "是" if ok else "不是", ["不是" if ok else "是", "只有偶數能判斷", "要看個位數"], ("%d ÷ %d ＝ %d，整除，是 %d 的倍數。" % (n, p, n // p, p)) if ok else ("%d ÷ %d ＝ %d……%d，不能整除。" % (n, p, n // p, n % p)))

    def pf():
        n = R.choice([x for x in range(30, 100) if x not in PR and least(x) >= 3])
        return mcq("%d 最小的質因數是多少？" % n, str(least(n)), [str(x) for x in (2, n // least(n), 1)  if x != least(n)] + ["9"], "%d 是奇數，2 不行；%d ÷ %d ＝ %d。" % (n, n, least(n), n // least(n)))
    return pick_unique(R, seven, 12, seen) + pick_unique(R, pf, 8, seen)


def s5(seen):
    def twin():
        a = R.choice([p for p in PR if p + 2 in PR and p > 3])
        return mcq("兩個質數相差 2，例如 3 和 5。下面哪一組也是？", "%d 和 %d" % (a, a + 2), ["%d 和 %d" % (x, x + 2) for x in R.sample([25, 33, 49, 91, 13 + 6, 51, 85, 115 - 30], 3)], "%d 和 %d 都是質數，相差 2。" % (a, a + 2))

    def card():
        a, b = R.sample([1, 3, 7, 9], 2)
        nums = [10 * a + b, 10 * b + a]
        pr = [x for x in nums if x in PR]
        q = "用數字卡 %d 和 %d 排成兩位數，可以排出幾個質數？" % (a, b)
        return mcq(q, "%d 個" % len(pr), ["%d 個" % x for x in (0, 1, 2, 3) if x != len(pr)], "可以排出 %d 和 %d，其中質數有 %s。" % (nums[0], nums[1], "、".join(map(str, pr)) if pr else "0 個"))

    def sum2():
        n = R.choice([x for x in range(20, 101, 2)])
        pairs = [(p, n - p) for p in PR if p <= n - p and (n - p) in PR]
        if not pairs:
            return None
        p, q2 = R.choice(pairs)
        return mcq("%d 可以寫成兩個質數的和。下面哪一組正確？" % n, "%d ＋ %d" % (p, q2), ["%d ＋ %d" % (p + 2, q2 - 2), "%d ＋ %d" % (1, n - 1), "%d ＋ %d" % (9, n - 9)], "%d 和 %d 都是質數，%d ＋ %d ＝ %d。" % (p, q2, p, q2, n))
    return pick_unique(R, twin, 1, seen) + pick_unique(R, card, 6, seen) + pick_unique(R, sum2, 13, seen)


def main():
    seen = set()
    sets = [("找出質數和合數", s1(seen)), ("篩法與質數的個數", s2(seen)), ("判斷質數要試除到哪裡", s3(seen)),
            ("倍數判別與最小質因數", s4(seen)), ("挑戰", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>質數</b>：大於 1，只有 1 和本身兩個因數。<b>合數</b>：還有其他因數。1 不是質數也不是合數。",
         "<b>篩法</b>：列出 2～100，留下 2、3、5、7，劃掉它們的倍數，剩下的就是質數（共 25 個）。",
         "判斷 n 是不是質數，只要用<b>不大於 √n 的質數</b>試除；100 以內試 2、3、5、7 就夠了。"],
        [example("91 是質數嗎？", ["試 2、3、5 都不行。", "91 ÷ 7 ＝ 13。"], "不是，91 ＝ 7 × 13"),
         example("97 是質數嗎？", ["試 2、3、5、7 都除不盡。"], "是質數")],
        [("51 是質數", "51 ＝ 3 × 17"),
         ("奇數都是質數", "9、15、21 都是奇數合數"),
         ("1 是質數", "1 只有一個因數")])
    faq = [{"q": "100 以內有哪些質數？",
            "a": "2、3、5、7、11、13、17、19、23、29、31、37、41、43、47、53、59、61、67、71、73、79、83、89、97，共 25 個。"},
           {"q": "為什麼試除到 √n 就夠了？",
            "a": "如果 n 是合數，一定有一個因數不超過 √n；所以小於等於 √n 的質數都除不盡，n 就是質數。"},
           {"q": "七年級的質數要學什麼？",
            "a": "108課綱 N-7-1：100 以內的質數，質數和合數的定義，以及質數的篩法。"}]
    make_unit(R, "grade-7", "primes", "N-7-1",
              "100 以內的質數：質數和合數的定義；質數的篩法。",
              "100 以內的質數",
              "七年級數學 質數 練習題｜100以內的質數・篩法・合數 學習單（附解答）",
              "100 以內的質數",
              "國中七年級數學「100 以內的質數」免費學習單：質數和合數的定義、篩法與質數的個數、判斷質數要試除到哪裡、7 和 11 的倍數與最小質因數，以及數字卡等挑戰題。100題線上練習馬上對答案，附可列印解答。",
              "質數只有 1 和本身兩個因數",
              "100 以內用 2、3、5、7 試除就夠了。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
