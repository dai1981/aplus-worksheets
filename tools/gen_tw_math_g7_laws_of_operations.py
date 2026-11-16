# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：數的運算規律（108課綱 N-7-4）
  python3 tools/gen_tw_math_g7_laws_of_operations.py
交換律・結合律（正數・負數をまとめる、湊整）、分配律（負數を含む）、－(a＋b)＝－a－b、－(a－b)＝－a＋b、簡便計算と判斷。
誤答：－(a－b) を －a－b とする、分配律で後ろの項に掛け忘れる、減法・除法で交換律を使う。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, par, opv, tidy_sets

R = random.Random(71006)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        a = R.randint(11, 89)
        b = -(100 - R.randint(1, 9)) if False else R.randint(11, 89)
        c = 100 - a
        d = -R.randint(11, 89)
        xs = [a, d, c]
        v = a + d + c
        q = "用簡便方法算：%s%s%s" % (sn(a), opv("＋", d), opv("＋", c))
        return mcq(q, sn(v), [sn(a - d + c), sn(-v), sn(v + 2)], "交換、結合：先算 %d ＋ %d ＝ 100，再 100%s ＝ %s。" % (a, c, opv("＋", d), sn(v)))

    def neg():
        xs = [nz(-40, 40) for _ in range(5)]
        v = sum(xs)
        pos = sum(x for x in xs if x > 0)
        ng = sum(x for x in xs if x < 0)
        q = "計算：" + sn(xs[0]) + "".join(opv("＋", x) for x in xs[1:])
        return mcq(q, sn(v), [sn(pos - ng), sn(-v), sn(v + 10)], "正數合起來 %s，負數合起來 %s，%s%s ＝ %s。" % (sn(pos), sn(ng), sn(pos), opv("＋", ng), sn(v)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, neg, 10, seen)


def s2(seen):
    def mk():
        a, b, c = nz(-9, 9), nz(-20, 20), nz(-20, 20)
        v = a * (b + c)
        q = "%s ×（%s%s）用分配律展開，結果是哪一個？" % (par(a), sn(b), opv("＋", c))
        ans = "%s × %s%s" % (par(a), par(b), opv("＋", a * c) if False else " ＋ %s × %s" % (par(a), par(c)))
        ans = "%s × %s ＋ %s × %s" % (par(a), par(b), par(a), par(c))
        w = ["%s × %s ＋ %s" % (par(a), par(b), par(c)), "%s × %s × %s" % (par(a), par(b), par(c)), "%s ＋ %s × %s" % (par(a), par(b), par(c))]
        return mcq(q, ans, w, "分配律：%s要分別乘括號裡的每一項。" % par(a))

    def calc():
        a = nz(-30, 30)
        b, c = R.choice([(37, 63), (48, 52), (125, -25), (99, 1), (-36, 136), (72, 28), (-15, 115)])
        v = a * (b + c)
        q = "用簡便方法算：%s × %s ＋ %s × %s" % (par(a), par(b), par(a), par(c))
        return mcq(q, sn(v), [sn(a * b + c), sn(-v), sn(v + a)], "＝ %s ×（%s%s）＝ %s × %s ＝ %s。" % (par(a), sn(b), opv("＋", c), par(a), sn(b + c), sn(v)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, calc, 10, seen)


def s3(seen):
    def mk():
        a, b = R.randint(2, 30), R.randint(2, 30)
        k = R.choice(["plus", "minus"])
        if k == "plus":
            q = "－（%d ＋ %d）去括號後是哪一個？" % (a, b)
            ans = "－%d － %d" % (a, b)
            w = ["－%d ＋ %d" % (a, b), "%d － %d" % (a, b), "－%d ＋（－%d）＋ 1" % (a, b) if False else "%d ＋ %d" % (a, b)]
            e = "－（a ＋ b）＝ －a － b：括號前是負號，去括號時裡面每一項都變號。"
        else:
            q = "－（%d － %d）去括號後是哪一個？" % (a, b)
            ans = "－%d ＋ %d" % (a, b)
            w = ["－%d － %d" % (a, b), "%d － %d" % (a, b), "%d ＋ %d" % (a, b)]
            e = "－（a － b）＝ －a ＋ b：裡面每一項都變號，－b 變成 ＋b。"
        return mcq(q, ans, w, e)

    def val():
        a, b, c = R.randint(10, 60), R.randint(2, 30), R.randint(2, 30)
        v = a - (b - c)
        q = "%d －（%d － %d）＝" % (a, b, c)
        return mcq(q, sn(v), [sn(a - b - c), sn(a + b - c), sn(-v)], "去括號：%d － %d ＋ %d ＝ %s。" % (a, b, c, sn(v)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, val, 10, seen)


def s4(seen):
    def mk():
        a = R.randint(101, 999)
        b = R.randint(11, 99)
        k = R.choice([1, 2])
        if k == 1:
            v = a - b - (a - b * 2)
            q = "用簡便方法算：%d － %d －（%d － %d）" % (a, b, a, 2 * b)
            e = "去括號：%d － %d － %d ＋ %d，%d 和 －%d 抵消，剩 －%d ＋ %d ＝ %s。" % (a, b, a, 2 * b, a, a, b, 2 * b, sn(v))
            w = [a - b - a - 2 * b, -v, 2 * a - 3 * b]
        else:
            c = R.choice([25, 125, 4, 8])
            m = {25: 4, 125: 8, 4: 25, 8: 125}[c]
            x = nz(-30, 30)
            v = c * x * m * -1
            q = "用簡便方法算：%d × %s × %s" % (c, par(x), par(-m))
            e = "交換、結合：%d × %s ＝ %s，再乘 %s ＝ %s。" % (c, par(-m), sn(-c * m), par(x), sn(v))
            w = [-v, c * x + m, v // 10 if v % 10 == 0 else v + 1]
        return mcq(q, sn(v), [sn(t) for t in w], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    OK = ["a ＋ b ＝ b ＋ a", "a × b ＝ b × a", "（a ＋ b）＋ c ＝ a ＋（b ＋ c）", "a ×（b ＋ c）＝ a × b ＋ a × c", "－（a ＋ b）＝ －a － b", "－（a － b）＝ －a ＋ b"]
    NG = ["a － b ＝ b － a", "a ÷ b ＝ b ÷ a", "－（a － b）＝ －a － b", "a ×（b ＋ c）＝ a × b ＋ c", "（a － b）－ c ＝ a －（b － c）", "－（a ＋ b）＝ －a ＋ b"]

    def mk():
        L = "甲乙丙丁"
        if R.random() < .5:
            ans = R.choice(OK)
            st = R.sample(NG, 3) + [ans]
            q = "下面哪一個<b>一定成立</b>？（a、b、c 是任意數，除數不為 0）"
        else:
            ans = R.choice(NG)
            st = R.sample(OK, 3) + [ans]
            q = "下面哪一個<b>不一定成立</b>？（a、b、c 是任意數，除數不為 0）"
        R.shuffle(st)
        k = st.index(ans)
        q += "<br>" + "<br>".join("%s：%s" % (L[i], t) for i, t in enumerate(st))
        return mcq(q, L[k], [x for x in L if x != L[k]], "%s：%s。加法和乘法有交換律、結合律；減法和除法沒有。去括號時，括號前是負號，裡面每一項都要變號。" % (L[k], ans))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("交換律和結合律", s1(seen)), ("分配律", s2(seen)), ("去括號", s3(seen)),
            ("簡便計算", s4(seen)), ("判斷規律", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["加法和乘法有<b>交換律、結合律</b>：可以換順序、先算方便的部分（湊成 100、把正數和負數分開加）。",
         "<b>分配律</b>：a ×（b ＋ c）＝ a × b ＋ a × c，a 是負數也一樣。",
         "去括號：<b>－（a ＋ b）＝ －a － b</b>，<b>－（a － b）＝ －a ＋ b</b>，括號裡每一項都變號。",
         "減法和除法沒有交換律、結合律。"],
        [example("38 ＋（－57）＋ 62", ["38 ＋ 62 ＝ 100。", "100 ＋（－57）＝ 43。"], "43"),
         example("50 －（30 － 8）", ["去括號：50 － 30 ＋ 8。"], "28")],
        [("－（30 － 8）＝ －30 － 8", "每一項都變號：－30 ＋ 8"),
         ("（－3）×（10 ＋ 2）＝ －30 ＋ 2", "2 也要乘 －3：－30 － 6"),
         ("10 － 3 ＝ 3 － 10", "減法不能交換")])
    faq = [{"q": "去括號時，什麼時候要變號？",
            "a": "括號前面是負號（或減號）時，去掉括號，裡面每一項都要變號；括號前面是正號就不變。"},
           {"q": "運算規律有什麼用？",
            "a": "可以讓計算變簡單，例如先把能湊成整十整百的數合起來，或用分配律把相同的乘數提出來。"},
           {"q": "七年級的運算規律要學什麼？",
            "a": "108課綱 N-7-4：交換律、結合律、分配律，以及 －(a＋b)＝－a－b、－(a－b)＝－a＋b。"}]
    make_unit(R, "grade-7", "laws-of-operations", "N-7-4",
              "數的運算規律：交換律；結合律；分配律；－(a＋b)＝－a－b；－(a－b)＝－a＋b。",
              "數的運算規律與去括號",
              "七年級數學 運算規律 練習題｜交換律・分配律・去括號 學習單（附解答）",
              "運算規律與去括號",
              "國中七年級數學「數的運算規律與去括號」免費學習單：交換律和結合律、含負數的分配律、－(a＋b) 和 －(a－b) 去括號、簡便計算與判斷規律。100題線上練習馬上對答案，附可列印解答。",
              "括號前是負號，去括號時每一項都變號",
              "－（a ＋ b）＝ －a － b；－（a － b）＝ －a ＋ b。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
