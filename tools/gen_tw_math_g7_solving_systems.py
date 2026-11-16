# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：二元一次聯立方程式的解法與應用（108課綱 A-7-5）
  python3 tools/gen_tw_math_g7_solving_systems.py
代入消去法（y＝… を代入）、加減消去法（係數をそろえて加減）、係數を倍にしてから消去、應用（票價・雞兔・和差・買い物）。
誤答：加減で符號を間違える（同號は減・異號は加）、倍にするとき右邊に掛け忘れる、x を求めて終わる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import sn, par, tidy_sets, term, const

R = random.Random(71016)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def eq2(a, b, c):
    return "%s%s ＝ %s" % (term(a, "x", True), term(b, "y"), sn(c))


def pt(x, y):
    return "x ＝ %s、y ＝ %s" % (sn(x), sn(y))


def sys_(e1, e2):
    return "<br>①　%s<br>②　%s" % (e1, e2)


def wrongs(x, y):
    return [pt(y, x), pt(-x, y), pt(x, -y), pt(x + 1, y - 1)]


def s1(seen):
    def mk():
        x, y = nz(-8, 8), nz(-8, 8)
        m, k = nz(-4, 4), nz(-6, 6)
        if y != m * x + k:
            y = m * x + k
        a, b = nz(-5, 5), nz(-5, 5)
        c = a * x + b * y
        if a + b * m == 0:
            return None
        e1 = "y ＝ %s%s" % (term(m, "x", True), const(k))
        q = "用代入消去法解：" + sys_(e1, eq2(a, b, c))
        return mcq(q, pt(x, y), [w for w in wrongs(x, y) if w != pt(x, y)][:3],
                   "把 ① 代入 ②：%s%s ×（%s%s）＝ %s，解得 x ＝ %s，再代回得 y ＝ %s。" % (term(a, "x", True), " ＋ %s" % sn(b) if b > 0 else " ＋（%s）" % sn(b), term(m, "x", True), const(k), sn(c), sn(x), sn(y)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        x, y = nz(-8, 8), nz(-8, 8)
        a = nz(-5, 5)
        b1, b2 = R.choice([(1, 1), (2, 2), (3, 3), (1, -1), (2, -2), (3, -3), (-1, 1), (-2, 2)])
        a2 = nz(-5, 5)
        if a == a2 and b1 == b2:
            return None
        c1, c2 = a * x + b1 * y, a2 * x + b2 * y
        how = "－" if b1 == b2 else "＋"
        nx = a - a2 if b1 == b2 else a + a2
        if nx == 0:
            return None
        q = "用加減消去法解：" + sys_(eq2(a, b1, c1), eq2(a2, b2, c2))
        return mcq(q, pt(x, y), [w for w in wrongs(x, y) if w != pt(x, y)][:3],
                   "y 的係數%s，① %s ② 消去 y：%s ＝ %s，x ＝ %s，再代回得 y ＝ %s。" % ("相同" if b1 == b2 else "互為相反數", how, term(nx, "x", True), sn(c1 - c2 if b1 == b2 else c1 + c2), sn(x), sn(y)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        x, y = nz(-6, 6), nz(-6, 6)
        a1, b1 = nz(-4, 4), R.choice([1, -1, 2, -2])
        a2, b2 = nz(-4, 4), b1 * R.choice([2, 3, -2, -3])
        if a1 * b2 == a2 * b1:
            return None
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        k = b2 // b1
        q = "解聯立方程式：" + sys_(eq2(a1, b1, c1), eq2(a2, b2, c2))
        return mcq(q, pt(x, y), [w for w in wrongs(x, y) if w != pt(x, y)][:3],
                   "① × %s：%s，再減去 ② 消去 y，得 x ＝ %s、y ＝ %s。（右邊也要乘！）" % (par(k), eq2(a1 * k, b1 * k, c1 * k), sn(x), sn(y)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def ticket():
        p1, p2 = R.choice([(250, 150), (300, 180), (200, 100), (320, 160)])
        n = R.randint(6, 15)
        a = R.randint(1, n - 1)
        t = p1 * a + p2 * (n - a)
        q = "全票 %d 元、半票 %d 元，共買 %d 張，付 %s 元。全票、半票各幾張？" % (p1, p2, n, num(t))
        ans = "全票 %d 張、半票 %d 張" % (a, n - a)
        alts = [(n - a, a), (a + 1, n - a - 1), (a - 1, n - a + 1), (a + 2, n - a - 2), (a - 2, n - a + 2)]
        return mcq(q, ans, ["全票 %d 張、半票 %d 張" % t for t in alts if min(t) >= 0],
                   "x ＋ y ＝ %d，%dx ＋ %dy ＝ %s，解得 x ＝ %d、y ＝ %d。" % (n, p1, p2, num(t), a, n - a))

    def sumdiff():
        x, y = R.randint(20, 90), R.randint(5, 60)
        if x <= y:
            return None
        q = "兩數的和是 %d，大數比小數的 2 倍少 %d。兩數各是多少？" % (x + y, 2 * y - x) if 2 * y > x else "兩數的和是 %d，大數比小數多 %d。兩數各是多少？" % (x + y, x - y)
        ans = "大數 %d、小數 %d" % (x, y)
        return mcq(q, ans, ["大數 %d、小數 %d" % (y, x), "大數 %d、小數 %d" % (x + 1, y - 1), "大數 %d、小數 %d" % (x - 2, y + 2)], "設大數 x、小數 y，列出兩個式子聯立解得 x ＝ %d、y ＝ %d。" % (x, y))
    return pick_unique(R, ticket, 10, seen) + pick_unique(R, sumdiff, 10, seen)


def s5(seen):
    def buy():
        a, b = R.randint(10, 60), R.randint(10, 60)
        if a == b:
            return None
        n1, m1, n2, m2 = R.randint(1, 4), R.randint(1, 4), R.randint(1, 4), R.randint(1, 4)
        if n1 * m2 == n2 * m1:
            return None
        t1, t2 = n1 * a + m1 * b, n2 * a + m2 * b
        item = R.choice([("蘋果", "梨子", "顆", "顆"), ("麵包", "牛奶", "個", "瓶"), ("原子筆", "筆記本", "枝", "本")])
        q = "買 %d %s%s和 %d %s%s要 %d 元；買 %d %s%s和 %d %s%s要 %d 元。一%s%s多少元？" % (n1, item[2], item[0], m1, item[3], item[1], t1, n2, item[2], item[0], m2, item[3], item[1], t2, item[2], item[0])
        return mcq(q, "%d 元" % a, ["%d 元" % v for v in (b, a + 5, abs(t1 - t2))  if v != a], "設%s x 元、%s y 元：%s，%s，解得 x ＝ %d、y ＝ %d。" % (item[0], item[1], eq2(n1, m1, t1), eq2(n2, m2, t2), a, b))

    def chick():
        h = R.randint(10, 40)
        r = R.randint(1, h - 1)
        legs = 2 * (h - r) + 4 * r
        q = "雞和兔共 %d 隻，腳共 %d 隻。兔有幾隻？" % (h, legs)
        return mcq(q, "%d 隻" % r, ["%d 隻" % v for v in (h - r, legs // 4, r + 2)  if v != r], "x ＋ y ＝ %d，2x ＋ 4y ＝ %d，第一式乘 2 再相減：2y ＝ %d，y ＝ %d。" % (h, legs, legs - 2 * h, r))
    return pick_unique(R, buy, 12, seen) + pick_unique(R, chick, 8, seen)


def main():
    seen = set()
    sets = [("代入消去法", s1(seen)), ("加減消去法", s2(seen)), ("先乘倍數再消去", s3(seen)),
            ("應用：票數和兩數", s4(seen)), ("應用：買東西和雞兔", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>代入消去法</b>：把一個式子寫成 y ＝ …（或 x ＝ …），代入另一式，變成一元一次方程式。",
         "<b>加減消去法</b>：某個未知數的係數相同就相減，互為相反數就相加，把它消掉。",
         "係數不一樣時，先把式子<b>整個乘以</b>一個數（左右兩邊都要乘），讓係數一樣。",
         "求出一個未知數後，代回原式求另一個，最後驗算。"],
        [example("｛x ＋ y ＝ 10；x － y ＝ 4", ["兩式相加：2x ＝ 14，x ＝ 7。", "代回：7 ＋ y ＝ 10，y ＝ 3。"], "x ＝ 7、y ＝ 3"),
         example("｛2x ＋ y ＝ 7；3x ＋ 2y ＝ 12", ["第一式乘 2：4x ＋ 2y ＝ 14。", "相減：x ＝ 2，y ＝ 3。"], "x ＝ 2、y ＝ 3")],
        [("y 係數都是 3，兩式相加", "係數相同要相減"),
         ("第一式乘 2 只乘左邊", "等號兩邊都要乘"),
         ("求出 x 就停了", "還要求 y，並驗算")])
    faq = [{"q": "代入消去法和加減消去法怎麼選？",
            "a": "有一個式子已經是 y ＝ … 或 x ＝ … 的形式，用代入法；兩式中有某個未知數的係數相同或相反，用加減法。"},
           {"q": "解完聯立方程式要怎麼驗算？",
            "a": "把 x、y 同時代入兩個原來的式子，兩邊都相等才對。"},
           {"q": "七年級的聯立方程式解法要學什麼？",
            "a": "108課綱 A-7-5：二元一次聯立方程式的代入消去法、加減消去法和應用問題。"}]
    make_unit(R, "grade-7", "solving-systems", "A-7-5",
              "二元一次聯立方程式的解法與應用：代入消去法；加減消去法；應用問題。",
              "二元一次聯立方程式的解法",
              "七年級數學 聯立方程式解法 練習題｜代入消去法・加減消去法 學習單（附解答）",
              "聯立方程式的解法",
              "國中七年級數學「二元一次聯立方程式的解法」免費學習單：代入消去法、加減消去法、先乘倍數再消去，以及票數、兩數、買東西和雞兔同籠的應用題。100題線上練習馬上對答案，附可列印解答。",
              "消去一個未知數，變成一元一次方程式",
              "係數相同相減、相反相加；乘倍數時等號兩邊都要乘。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
