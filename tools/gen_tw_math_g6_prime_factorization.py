# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：質數與質因數分解（108課綱 N-6-1）
  python3 tools/gen_tw_math_g6_prime_factorization.py
20 以內的質數與合數、2・3・5 の倍數判別、質因數、短除法で質因數分解、指數なしの積で表す。
誤答：1 を質數とする、9・15 を質數とする、短除法で合數で割って止める、因數と質因數を取り違える。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(61001)
NM = Names(R)
PR = [2, 3, 5, 7, 11, 13, 17, 19]


def factor(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def prod(fs):
    return " × ".join(map(str, fs))


def s1(seen):
    def which():
        kind = R.choice(["prime", "comp"])
        if kind == "prime":
            ans = R.choice(PR)
            w = R.sample([1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20], 3)
            return mcq("下面哪一個數是<b>質數</b>？（%s）" % "、".join(map(str, sorted(w + [ans]))), str(ans), [str(x) for x in w],
                       "%d 只有 1 和 %d 兩個因數，是質數。%s" % (ans, ans, "1 只有 1 個因數，不是質數。" if 1 in w else "其他的數還有別的因數。"))
        ans = R.choice([4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
        w = R.sample([1] + PR, 3)
        fs = [d for d in range(2, ans) if ans % d == 0]
        return mcq("下面哪一個數是<b>合數</b>？（%s）" % "、".join(map(str, sorted(w + [ans]))), str(ans), [str(x) for x in w],
                   "%d 除了 1 和 %d，還有因數 %s，是合數。" % (ans, ans, "、".join(map(str, fs))))

    def count():
        F = [("20 以內一共有幾個質數？", "8 個", ["9 個", "7 個", "10 個"], "2、3、5、7、11、13、17、19，共 8 個。"),
             ("1 是質數還是合數？", "都不是", ["質數", "合數", "既是質數也是合數"], "1 只有一個因數（1），所以 1 既不是質數，也不是合數。"),
             ("哪一個質數是偶數？", "2", ["4", "1", "沒有"], "2 只有 1 和 2 兩個因數，是唯一的偶數質數。"),
             ("10 以內有哪些質數？", "2、3、5、7", ["1、3、5、7", "2、3、5、7、9", "3、5、7、9"], "1 不是質數，9 ＝ 3 × 3 是合數。"),
             ("11 到 20 之間有哪些質數？", "11、13、17、19", ["11、13、15、17、19", "13、17、19", "11、13、17"], "15 ＝ 3 × 5 是合數。"),
             ("9 為什麼不是質數？", "9 ＝ 3 × 3，還有因數 3", ["9 是奇數", "9 比 10 小", "9 不能被 2 整除"], "質數只有 1 和自己兩個因數；9 還有因數 3。")]
        return mcq(*R.choice(F))
    return pick_unique(R, which, 14, seen) + pick_unique(R, count, 6, seen)


def s2(seen):
    def mk():
        p = R.choice([2, 3, 5])
        n = R.randint(100, 9999)
        rule = {2: "個位是 0、2、4、6、8", 3: "各位數字的和是 3 的倍數", 5: "個位是 0 或 5"}[p]
        if p == 3:
            n = n - n % 3 if R.random() < .5 else n
        q = "%s 是不是 %d 的倍數？" % (num(n), p)
        ok = n % p == 0
        if p == 3:
            ds = sum(int(c) for c in str(n))
            e = "各位數字的和：%s ＝ %d，%s 3 的倍數，所以%s。" % (" ＋ ".join(str(n)), ds, "是" if ds % 3 == 0 else "不是", "是" if ok else "不是")
        else:
            e = "%d 的倍數：%s。%s 的個位是 %d，所以%s。" % (p, rule, num(n), n % 10, "是" if ok else "不是")
        return mcq(q, "是" if ok else "不是", ["不是" if ok else "是", "要算出來才知道", "只有偶數才能判斷"], e)

    def pick():
        p = R.choice([2, 3, 5])
        cands = []
        while len(cands) < 4:
            x = R.randint(100, 999)
            if x not in cands:
                cands.append(x)
        good = [x for x in cands if x % p == 0]
        if len(good) != 1:
            return None
        ans = good[0]
        rule = {2: "個位是偶數", 3: "各位數字的和是 3 的倍數", 5: "個位是 0 或 5"}[p]
        return mcq("%s 中，哪一個數是 %d 的倍數？" % ("、".join(map(str, cands)), p), str(ans), [str(x) for x in cands if x != ans], "%d 的倍數：%s。%d 符合。" % (p, rule, ans))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, pick, 10, seen)


def s3(seen):
    def mk():
        n = R.randint(12, 120)
        fs = factor(n)
        if len(fs) < 2 or max(fs) > 19:
            return None
        divs = [d for d in range(2, n) if n % d == 0]
        kind = R.choice(["pf", "notpf"])
        if kind == "pf":
            ps = sorted(set(fs))
            ans = "、".join(map(str, ps))
            comp = [d for d in divs if d not in ps]
            if not comp:
                return None
            j = lambda xs: "、".join(map(str, xs))
            w = [j(sorted(set(ps) | {comp[0]})), "1、" + ans, j(divs), j(ps[:-1]) if len(ps) > 1 else j(sorted(ps + [next(q for q in PR if q not in ps)]))]
            w = [x for x in dict.fromkeys(w) if x != ans]
            return mcq("%d 的質因數有哪些？" % n, ans, w, "%d ＝ %s，質因數是 %s（因數裡是質數的那些）。" % (n, prod(fs), ans))
        comp = [d for d in divs if d not in fs]
        if not comp:
            return None
        bad = R.choice(comp)
        ps = sorted(set(fs))
        opts = ps[:3]
        if len(opts) < 3:
            return None
        return mcq("下面哪一個<b>不是</b> %d 的質因數？" % n, str(bad), [str(x) for x in opts], "%d 雖然是 %d 的因數，但 %d 是合數，不是質因數。" % (bad, n, bad))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        n = R.choice([x for x in range(24, 400) if len(factor(x)) >= 3 and max(factor(x)) <= 19])
        fs = factor(n)
        ans = prod(fs)
        c = [d for d in range(4, n) if n % d == 0 and len(factor(d)) >= 2]
        w = []
        if c:
            d = c[0]
            w.append(prod(sorted(factor(n // d) + [d])))
        w.append(prod(fs[:-1]))
        w.append(prod(sorted(fs + [fs[0]])))
        w.append("1 × " + ans)
        return mcq("用短除法把 %d 做質因數分解，結果是哪一個？" % n, ans, w,
                   "一直用質數去除到商是 1：%d ＝ %s。每個乘數都要是質數。" % (n, ans))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def back():
        fs = sorted(R.choices([2, 3, 5, 7], k=R.randint(3, 4)))
        n = 1
        for f in fs:
            n *= f
        if n > 1000:
            return None
        return mcq("一個數的質因數分解是 %s，這個數是多少？" % prod(fs), num(n), [num(x) for x in (sum(fs), n + fs[0], n // fs[-1] if n // fs[-1] != n else n * 2, n * fs[0])],
                   "把質因數全部乘起來：%s ＝ %s。" % (prod(fs), num(n)))

    def rect():
        n = R.choice([x for x in range(12, 60) if not len(factor(x)) == 1])
        pairs = [(a, n // a) for a in range(1, int(n ** .5) + 1) if n % a == 0]
        who = NM.next()
        q = "%s用 %d 個一樣大的正方形排成長方形（排滿、不能剩）。一共有幾種不同的排法？（長寬對調算同一種）" % (who, n)
        k = len(pairs)
        return mcq(q, "%d 種" % k, ["%d 種" % x for x in (k + 1, k * 2, k - 1 if k > 1 else k + 2)], "%d 的因數成對：%s，共 %d 種。" % (n, "、".join("%d×%d" % p for p in pairs), k))

    def cnt():
        n = R.choice([x for x in range(30, 200) if len(set(factor(x))) >= 2 and max(factor(x)) <= 19])
        ps = sorted(set(factor(n)))
        return mcq("%d 有幾個不同的質因數？" % n, "%d 個" % len(ps), ["%d 個" % x for x in (len(factor(n)), len([d for d in range(1, n + 1) if n % d == 0]), len(ps) + 1) if x != len(ps)] + ["%d 個" % (len(ps) + 2)],
                   "%d ＝ %s，不同的質因數是 %s，共 %d 個。" % (n, prod(factor(n)), "、".join(map(str, ps)), len(ps)))
    return pick_unique(R, back, 7, seen) + pick_unique(R, rect, 7, seen) + pick_unique(R, cnt, 6, seen)


def main():
    seen = set()
    sets = [("質數和合數", s1(seen)), ("2、3、5 的倍數判別", s2(seen)), ("質因數", s3(seen)),
            ("用短除法做質因數分解", s4(seen)), ("應用", s5(seen))]
    body = lesson(
        ["<b>質數</b>：只有 1 和自己兩個因數（2、3、5、7、11、13、17、19）。<b>合數</b>：還有別的因數。1 兩者都不是。",
         "判別：2 的倍數個位是偶數；5 的倍數個位是 0 或 5；3 的倍數各位數字的和是 3 的倍數。",
         "<b>質因數分解</b>：用短除法一直用質數去除，到商是 1 為止，把除數乘起來。"],
        [example("把 60 做質因數分解。", ["60 ÷ 2 ＝ 30，30 ÷ 2 ＝ 15，15 ÷ 3 ＝ 5，5 ÷ 5 ＝ 1。"], "60 ＝ 2 × 2 × 3 × 5"),
         example("483 是不是 3 的倍數？", ["4 ＋ 8 ＋ 3 ＝ 15，15 是 3 的倍數。"], "是")],
        [("1 是質數", "1 只有一個因數，不是質數也不是合數"),
         ("60 ＝ 4 × 3 × 5", "4 不是質數，要再分成 2 × 2"),
         ("9、15 是質數", "9 ＝ 3 × 3，15 ＝ 3 × 5，都是合數")])
    faq = [{"q": "怎麼判斷一個數是不是質數？",
            "a": "看它除了 1 和自己以外，能不能被 2、3、5、7 等較小的質數整除；能整除就是合數。"},
           {"q": "什麼是短除法？",
            "a": "把數寫在右邊，左邊寫能整除它的質數，商寫在下面，一直除到商是 1，左邊的質數乘起來就是質因數分解。"},
           {"q": "六年級為什麼要學質因數分解？",
            "a": "108課綱 N-6-1、N-6-2：質因數分解可以用來找最大公因數和最小公倍數，再用在分數的約分和通分。"}]
    make_unit(R, "grade-6", "prime-factorization", "N-6-1",
              "20 以內的質數和質因數分解：小於 20 的質數與合數。2、3、5 的質因數判別法。以短除法做質因數的分解。",
              "質數與質因數分解",
              "六年級數學 質因數分解 練習題｜質數・合數・短除法 學習單（附解答）",
              "質因數分解",
              "國小六年級數學「質數與質因數分解」免費學習單：20 以內的質數和合數、2、3、5 的倍數判別、質因數、用短除法做質因數分解與應用。100題線上練習馬上對答案，附可列印解答。",
              "質數只有 1 和自己兩個因數",
              "質因數分解：用短除法一直除到商是 1。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
