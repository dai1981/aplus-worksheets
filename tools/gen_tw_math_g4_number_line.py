# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：數線與分數、小數（108課綱 N-4-8）
  python3 tools/gen_tw_math_g4_number_line.py
數線上の分數（假分數・帶分數）と小數を読む、同じ點を分數と小數で表す、比大小、數線上の加減。
誤答：目盛りの数ではなく線の数で数える（1/6 と 1/5）、0.1 刻みと 0.01 刻みの取り違え、整数部分を忘れる。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, mx, fig, svg_wrap, text, line, dnum, INK, RED, BLUE

R = random.Random(41009)
NM = Names(R)
X0, X1 = 30, 490


def nl(lo, hi, n, labels, marks=(), jump=None):
    """lo〜hi（整数）を n 等分。labels：{目盛り番号: 文字}"""
    gap = (X1 - X0) / n
    s = [line(X0 - 10, 50, X1 + 14, 50, INK, 2), "<polygon points='%d,44 %d,50 %d,56' fill='%s'/>" % (X1 + 14, X1 + 24, X1 + 14, INK)]
    per = n // (hi - lo)
    for i in range(n + 1):
        x = X0 + i * gap
        big = i % per == 0
        s.append(line(x, 40 if big else 44, x, 60 if big else 56, INK, 2 if big else 1.4))
        if i in labels:
            s.append(text(x, 82, labels[i], 15))
    for i, t, col in marks:
        x = X0 + i * gap
        s.append("<polygon points='%.1f,38 %.1f,24 %.1f,24' fill='%s'/>" % (x, x - 7, x + 7, col))
        s.append(text(x, 18, t, 15, col=col))
    if jump:
        a, b = jump
        xa, xb = X0 + a * gap, X0 + b * gap
        s.append("<path d='M%.1f 40 Q%.1f %d %.1f 40' fill='none' stroke='%s' stroke-width='2.5'/>" % (xa, (xa + xb) / 2, 4, xb, BLUE))
    return fig(svg_wrap(520, 92, "".join(s), "數線"))


def fv(v, d=None):
    v = F(v)
    d = d or v.denominator
    n = v * d
    w, r = divmod(int(n), d)
    return str(w) if r == 0 else (mx(w, r, d) if w else fr(r, d))


def s1(seen):
    def mk():
        hi = R.choice([1, 2, 3])
        per = R.choice([3, 4, 5, 6, 8]) if hi < 3 else R.choice([3, 4, 5])
        n = hi * per
        k = R.randint(1, n - 1)
        if k % per == 0:
            return None
        lab = {i * per: str(i) for i in range(hi + 1)}
        q = "箭頭指的數是多少？（用分數表示）" + nl(0, hi, n, lab, [(k, "?", RED)])
        v = F(k, per)
        return mcq(q, fv(v, per), [fv(F(k, per + 1), per + 1), fv(F(k + 1, per), per) if (k + 1) % per else fv(F(k - 1, per), per), fr(k, n) if hi > 1 else fv(F(k, per - 1), per - 1) if per > 2 else fr(k, 10), fr(k, per) if v > 1 else fv(F(per - k, per), per)],
                   "0 到 1 平分成 %d 格，1 格是 %s。箭頭在第 %d 格：%s%s。" % (per, fr(1, per), k, fr(k, per), " ＝ " + fv(v, per) if k > per else ""))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        hi = R.choice([1, 1, 2, 3])
        tenth = R.random() < .6
        if tenth:
            n = hi * 10
            k = R.randint(1, n - 1)
            if k % 10 == 0:
                return None
            lab = {i * 10: str(i) for i in range(hi + 1)}
            q = "箭頭指的數是多少？（用小數表示）" + nl(0, hi, n, lab, [(k, "?", RED)])
            v = dnum(k / 10, 1)
            return mcq(q, v, [dnum(k / 100, 2), str(k), dnum((k + 1) / 10, 1), dnum((k - 1) / 10, 1) if k > 1 else dnum(k / 10 + 1, 1)],
                       "1 平分成 10 格，1 格是 0.1。箭頭在第 %d 格：%s。" % (k, v))
        lo = R.randint(0, 5)
        k = R.randint(1, 9)
        q = "箭頭指的數是多少？" + nl(0, 1, 10, {0: "%d.1" % lo if False else dnum(lo + .1, 1), 10: dnum(lo + .2, 1)}, [(k, "?", RED)])
        v = dnum(lo + .1 + k / 100, 2)
        return mcq(q, v, [dnum(lo + .1 + k / 10, 1) if k < 10 else v, dnum(lo + k / 100, 2), dnum(lo + .1 + (k + 1) / 100, 2), "%d.1%d0" % (lo, k)],
                   "%s 到 %s 平分成 10 格，1 格是 0.01。從 %s 往右 %d 格：%s。" % (dnum(lo + .1, 1), dnum(lo + .2, 1), dnum(lo + .1, 1), k, v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def same():
        P = [(1, 2, "0.5"), (1, 5, "0.2"), (2, 5, "0.4"), (3, 5, "0.6"), (4, 5, "0.8"), (1, 4, "0.25"), (3, 4, "0.75")]
        a, b, dv = R.choice(P)
        w = R.randint(0, 3)
        num_ = w * b + a
        f = mx(w, a, b) if w else fr(a, b)
        d = dnum(w + float(dv), 2)
        if R.random() < .5:
            q = "數線上 %s 的位置，也可以用哪一個小數表示？" % f
            return mcq(q, d, [dnum(w + a / 10, 1) if dnum(w + a / 10, 1) != d else dnum(w + .1, 1), "%d.%d%d" % (w, a, b), dnum(w + b / 10, 1) if b < 10 else d + "1", dnum(w + 1 + float(dv), 2)],
                       ("%s ＝ %s，所以 %s ＝ %s。" % (fr(a, b), dv, f, d)) if w else "%s ＝ %s ＝ %s。" % (fr(a, b), fr(int(float(dv) * 100), 100) if len(dv) == 4 else fr(int(float(dv) * 10), 10), dv))
        q = "數線上 %s 的位置，也可以用哪一個分數表示？" % d
        return mcq(q, f, [mx(w, b, a) if w and a > 1 and b > a else fr(b, a) if a > 1 else fr(1, b + 1), mx(w + 1, a, b), fr(int(float(dv) * 10), 100) if w == 0 else mx(w, a, b + 1)],
                   ("%s ＝ %s，所以 %s ＝ %s。" % (dv, fr(a, b), d, f)) if w else "%s ＝ %s ＝ %s。" % (dv, fr(int(float(dv) * 100), 100) if len(dv) == 4 else fr(int(float(dv) * 10), 10), f))

    def cmp_():
        d = R.choice([2, 4, 5, 10])
        a = R.randint(1, 3 * d)
        b = R.randint(1, 29) / 10
        x = F(a, d)
        if x == F(b).limit_denominator(100) or a % d == 0:
            return None
        sign = ">" if x > F(b).limit_denominator(100) else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % (fv(x, d), dnum(b, 1)), sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "%s ＝ %s，在數線上越右邊越大：%s %s %s。" % (fv(x, d), dnum(float(x), 2), fv(x, d), sign, dnum(b, 1)))
    return pick_unique(R, same, 10, seen) + pick_unique(R, cmp_, 10, seen)


def s4(seen):
    def mk():
        per = R.choice([4, 5, 10])
        hi = 2
        n = hi * per
        a = R.randint(1, n - 3)
        b = R.randint(2, n - a)
        add = R.random() < .6
        if not add:
            a, b = a + b, b
        to = a + b if add else a - b
        if to <= 0 or to > n:
            return None
        lab = {0: "0", per: "1", 2 * per: "2"}
        if per == 10:
            sa, sb, st = dnum(a / 10, 1), dnum(b / 10, 1), dnum(to / 10, 1)
            wrong = [dnum((to + 1) / 10, 1), dnum((to - 1) / 10, 1) if to > 1 else dnum((to + 2) / 10, 1), dnum((a - b) / 10, 1) if add and a > b else dnum((a + b) / 10, 1) if not add else dnum((to + 2) / 10, 1)]
        else:
            sa, sb, st = fv(F(a, per), per), fv(F(b, per), per), fv(F(to, per), per)
            wrong = [fv(F(to + 1, per), per), fv(F(to - 1, per), per) if to > 1 else fv(F(to + 2, per), per), fr(a + b if add else a - b, per * 2) if (a + b if add else a - b) > 0 else fv(F(to + 2, per), per)]
        q = "看數線，%s %s %s ＝？" % (sa, "＋" if add else "－", sb) + nl(0, hi, n, lab, (), (a, to))
        return mcq(q, st, wrong, "從 %s %s跳 %d 格（%s），到 %s。" % (sa, "往右" if add else "往左", b, sb, st))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def walk():
        per = R.choice([4, 5, 10])
        a = R.randint(1, 2 * per - 1)
        b = R.randint(1, 2 * per - a)
        who = NM.next()
        unit = "公里"
        if per == 10:
            sa, sb, st = dnum(a / 10, 1), dnum(b / 10, 1), dnum((a + b) / 10, 1)
            w = [dnum((a + b) / 100, 2), dnum((a + b + 1) / 10, 1), dnum(abs(a - b) / 10, 1) if a != b else dnum((a + b + 2) / 10, 1)]
        else:
            sa, sb, st = fv(F(a, per), per), fv(F(b, per), per), fv(F(a + b, per), per)
            w = [fr(a + b, 2 * per), fv(F(a + b + 1, per), per), fv(F(abs(a - b), per), per) if a != b else fv(F(a + b + 2, per), per)]
        q = "%s從家走到公園是 %s 公里，再從公園走到圖書館是 %s 公里。從家到圖書館一共走了幾公里？" % (who, sa, sb)
        return mcq(q, st + " 公里", [x + " 公里" for x in w], "%s ＋ %s ＝ %s（公里）。" % (sa, sb, st))

    def between():
        a = R.randint(1, 8)
        q = "下面哪一個數在 %s 和 %s 之間？" % (dnum(a / 10, 1), dnum((a + 1) / 10, 1))
        k = R.randint(1, 9)
        good = dnum(a / 10 + k / 100, 2)
        return mcq(q, good, [dnum((a + 1) / 10 + k / 100, 2), dnum(a / 100 + k / 1000, 3) if a else "0.0%d" % k, dnum(a + k / 10, 1)],
                   "%s ＝ %s，%s ＝ %s，中間是 %s 到 %s，%s 在中間。" % (dnum(a / 10, 1), "%.2f" % (a / 10), dnum((a + 1) / 10, 1), "%.2f" % ((a + 1) / 10), "%.2f" % (a / 10), "%.2f" % ((a + 1) / 10), good))
    return pick_unique(R, walk, 12, seen) + pick_unique(R, between, 8, seen)


def main():
    seen = set()
    sets = [("數線上的分數", s1(seen)), ("數線上的小數", s2(seen)), ("分數和小數在同一個位置", s3(seen)),
            ("在數線上加減", s4(seen)), ("應用問題", s5(seen))]
    demo = nl(0, 2, 10, {0: "0", 5: "1", 10: "2"}, [(7, "?", RED)])
    body = lesson(
        ["先看 0 到 1 之間平分成<b>幾格</b>：5 格就是 1 格 %s，10 格就是 1 格 0.1。" % fr(1, 5),
         "超過 1 的點，可以寫成假分數或帶分數：%s ＝ %s。" % (fr(7, 5), mx(1, 2, 5)),
         "同一個點可以用分數，也可以用小數表示：%s ＝ 0.5，%s ＝ 0.4。數線上越右邊的數越大。" % (fr(1, 2), fr(2, 5))],
        [example("箭頭指的數是多少？" + demo, ["0 到 1 平分成 5 格，1 格是 %s。" % fr(1, 5), "箭頭在第 7 格：%s ＝ %s。" % (fr(7, 5), mx(1, 2, 5))], mx(1, 2, 5) + "（1.4）"),
         example("0.6 和 %s 哪一個大？" % fr(3, 4), ["%s ＝ 0.75。" % fr(3, 4), "0.75 ＞ 0.6。"], fr(3, 4))],
        [("數刻度線有幾條，當成平分成幾格", "要數「格子」：6 條線之間只有 5 格"),
         ("1 後面的點只寫成真分數", "要加上整數：1 又幾分之幾"),
         ("0.1 和 0.01 的刻度弄混", "看兩個標好的數之間平分成幾格")])
    faq = [{"q": "四年級的數線要學什麼？",
            "a": "108課綱 N-4-8：在數線上標示和比較整數、分數、小數，並理解它們可以表示同一個位置，建立「整數、分數、小數是一體的」概念。"},
           {"q": "孩子讀數線上的分數常常讀錯，怎麼辦？",
            "a": "先找 0 和 1，數這兩點之間有「幾格」（不是幾條線），1 格就是幾分之一，再往右數。"},
           {"q": "分數和小數怎麼比大小？",
            "a": "化成同一種表示再比：3/4 ＝ 0.75，0.75 ＞ 0.6。也可以畫在數線上，越右邊越大。"}]
    make_unit(R, "grade-4", "number-line", "N-4-8",
              "數線與分數、小數：連結分小數長度量的經驗。以標記和簡單的比較與計算，建立整數、分數、小數一體的認識。",
              "數線與分數、小數",
              "四年級數學 數線 練習題｜數線上的分數和小數・比大小 學習單（附解答）",
              "數線與分數、小數",
              "國小四年級數學「數線與分數、小數」免費學習單：讀數線上的分數和小數、同一個位置的分數和小數、比大小和在數線上加減。100題線上練習馬上對答案，附可列印解答。",
              "先數 0 到 1 平分成幾格",
              "同一個點，可以寫成分數，也可以寫成小數。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
