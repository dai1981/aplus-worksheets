# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：數量關係的表示（108課綱 R-6-3、R-6-2）
  python3 tools/gen_tw_math_g6_quantity_relationships.py
表から二つの量の關係を見つける（和一定・差一定・倍數・倍數＋常數）、文字や記號で關係式を書く、關係式に代入、火柴棒など模式の關係式、應用。
誤答：最初の一組だけで決める、和一定と差一定を取り違える、□×3＋1 の ＋1 を忘れる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, num

R = random.Random(61015)
NM = Names(R)


def rule():
    k = R.choice(["sum", "diff", "mul", "lin"])
    if k == "sum":
        c = R.randint(10, 30)
        return k, c, None, (lambda x: c - x), "○ ＝ %d － □" % c, ["○ ＝ □ ＋ %d" % c, "○ ＝ %d × □" % c, "○ ＝ □ － %d" % c], "□ ＋ ○ 一直是 %d" % c
    if k == "diff":
        c = R.randint(2, 15)
        return k, c, None, (lambda x: x + c), "○ ＝ □ ＋ %d" % c, ["○ ＝ □ × %d" % c, "○ ＝ %d － □" % c, "○ ＝ □ － %d" % c], "○ 一直比 □ 多 %d" % c
    if k == "mul":
        c = R.randint(2, 9)
        return k, c, None, (lambda x: x * c), "○ ＝ □ × %d" % c, ["○ ＝ □ ＋ %d" % c, "○ ＝ □ ÷ %d" % c, "○ ＝ □ × %d ＋ 1" % c], "○ 一直是 □ 的 %d 倍" % c
    a, b = R.randint(2, 6), R.randint(1, 9)
    return k, a, b, (lambda x: a * x + b), "○ ＝ □ × %d ＋ %d" % (a, b), ["○ ＝ □ ＋ %d" % (a + b), "○ ＝ □ × %d" % (a + b), "○ ＝（□ ＋ %d）× %d" % (b, a)], "□ 每多 1，○ 就多 %d；□ × %d 再加 %d" % (a, a, b)


def xs(k):
    if k == "sum":
        st = R.randint(1, 3)
        return [st, st + 1, st + 2, st + 3, st + 4]
    st = R.randint(1, 4)
    return [st, st + 1, st + 2, st + 3, st + 4]


def s1(seen):
    def mk():
        k, a, b, f, ans, w, why = rule()
        x = xs(k)
        tb = table(["□"] + [str(v) for v in x], [["○"] + [str(f(v)) for v in x]])
        n = x[-1] + R.randint(2, 6)
        v = f(n)
        if v < 0:
            return None
        q = "看下表的規律，□ ＝ %d 時，○ 是多少？" % n + tb
        last = f(x[-1])
        return mcq(q, str(v), [str(t) for t in (last + (n - x[-1]), v + 1, n * 2) if t != v and t >= 0] + [str(v + 2)], "%s，所以 □ ＝ %d 時，○ ＝ %d。" % (why, n, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        k, a, b, f, ans, w, why = rule()
        x = xs(k)
        tb = table(["□"] + [str(v) for v in x], [["○"] + [str(f(v)) for v in x]])
        q = "下表中 □ 和 ○ 的關係式是哪一個？" + tb
        return mcq(q, ans, w, "%s：%s。每一組都要檢查。" % (why, ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def words():
        F_ = [("哥哥比弟弟大 %d 歲。弟弟 □ 歲時，哥哥 ○ 歲。關係式是哪一個？", "○ ＝ □ ＋ %d", ["○ ＝ □ － %d", "○ ＝ □ × %d", "□ ＝ ○ ＋ %d"], "哥哥一直比弟弟大 %d 歲。"),
              ("一枝筆 %d 元，買 □ 枝要付 ○ 元。關係式是哪一個？", "○ ＝ □ × %d", ["○ ＝ □ ＋ %d", "○ ＝ □ ÷ %d", "□ ＝ ○ × %d"], "總價 ＝ 單價 × 數量，%d 元乘以枝數。"),
              ("%d 顆糖分成兩堆，一堆 □ 顆，另一堆 ○ 顆。關係式是哪一個？", "○ ＝ %d － □", ["○ ＝ □ － %d", "○ ＝ □ ＋ %d", "○ ＝ %d × □"], "兩堆合起來一直是 %d 顆。"),
              ("一條繩子 %d 公分，剪掉 □ 公分，剩下 ○ 公分。關係式是哪一個？", "○ ＝ %d － □", ["○ ＝ □ － %d", "○ ＝ %d ÷ □", "○ ＝ □ ＋ %d"], "剪掉的和剩下的合起來是 %d 公分。"),
              ("一個正方形的邊長 □ 公分，周長 ○ 公分。關係式是哪一個？", "○ ＝ □ × 4", ["○ ＝ □ ＋ 4", "○ ＝ □ × □", "□ ＝ ○ × 4"], "周長是邊長的 4 倍。")]
        t = R.choice(F_)
        c = R.randint(3, 60)
        fmt = lambda x: x % c if "%d" in x else x
        return mcq(fmt(t[0]), fmt(t[1]), [fmt(x) for x in t[2]], fmt(t[3]))
    return pick_unique(R, words, 20, seen)


def s4(seen):
    def stick():
        kind = R.choice([("三角形", 2, 1), ("正方形", 3, 1), ("五邊形", 4, 1)])
        name, a, b = kind
        n = R.randint(5, 30)
        tot = a * n + b
        q = "用火柴棒排一排連在一起的%s：1 個用 %d 根，每多 1 個再多 %d 根。排 %d 個要幾根？" % (name, a + b, a, n)
        return mcq(q, "%d 根" % tot, ["%d 根" % x for x in ((a + b) * n, a * n, tot + a)], "根數 ＝ 個數 × %d ＋ 1：%d × %d ＋ 1 ＝ %d（根）。" % (a, n, a, tot))

    def table_seat():
        n = R.randint(4, 20)
        tot = 2 * n + 2
        q = "長方形桌子一張可以坐 4 人（長邊各 1 人、短邊各 1 人）。%d 張桌子排成一長排，最多坐幾人？" % n
        return mcq(q, "%d 人" % tot, ["%d 人" % x for x in (4 * n, 2 * n, tot + 2)], "長邊每張 2 人，加上兩端各 1 人：%d × 2 ＋ 2 ＝ %d（人）。" % (n, tot))

    def find_n():
        a = R.choice([2, 3, 4])
        n = R.randint(5, 25)
        tot = a * n + 1
        q = "照規律排圖形，第 □ 個要用 ○ 根火柴棒，關係式是 ○ ＝ □ × %d ＋ 1。用了 %d 根，是第幾個？" % (a, tot)
        return mcq(q, "第 %d 個" % n, ["第 %d 個" % x for x in (tot // a, n + 1, tot - a)  if x != n], "（%d － 1）÷ %d ＝ %d。" % (tot, a, n))
    return pick_unique(R, stick, 7, seen) + pick_unique(R, table_seat, 6, seen) + pick_unique(R, find_n, 7, seen)


def s5(seen):
    def plug():
        a, b = R.randint(2, 9), R.randint(1, 30)
        x = R.randint(2, 20)
        q = "關係式 ○ ＝ □ × %d ＋ %d。當 □ ＝ %d 時，○ 是多少？" % (a, b, x)
        v = a * x + b
        return mcq(q, str(v), [str(t) for t in (a * (x + b), x + a + b, a * x)], "%d × %d ＋ %d ＝ %d。" % (x, a, b, v))

    def back():
        a, b = R.randint(2, 9), R.randint(1, 20)
        x = R.randint(2, 20)
        v = a * x + b
        q = "關係式 ○ ＝ □ × %d ＋ %d。當 ○ ＝ %d 時，□ 是多少？" % (a, b, v)
        return mcq(q, str(x), [str(t) for t in (v * a + b, v // a if v // a != x else x + 2, v - b)], "（%d － %d）÷ %d ＝ %d。" % (v, b, a, x))

    def taxi():
        base, per = R.choice([(85, 5), (70, 5), (100, 10)])
        n = R.randint(3, 20)
        q = "計程車起跳 %d 元，之後每跳一次加 %d 元。跳了 □ 次，車資 ○ 元。跳 %d 次要付多少元？" % (base, per, n)
        v = base + per * n
        return mcq(q, "%d 元" % v, ["%d 元" % t for t in ((base + per) * n, base * n, per * n)], "○ ＝ %d ＋ □ × %d ＝ %d ＋ %d × %d ＝ %d（元）。" % (base, per, base, n, per, v))
    return pick_unique(R, plug, 7, seen) + pick_unique(R, back, 7, seen) + pick_unique(R, taxi, 6, seen)


def main():
    seen = set()
    sets = [("找出表中的規律", s1(seen)), ("寫出關係式", s2(seen)), ("把情境寫成關係式", s3(seen)),
            ("圖形模式", s4(seen)), ("用關係式求值", s5(seen))]
    body = lesson(
        ["兩個一起變化的量，用 □ 和 ○ 表示，把它們的關係寫成<b>關係式</b>。",
         "看表時，檢查每一組：<b>和一樣</b>（○ ＝ 10 － □）、<b>差一樣</b>（○ ＝ □ ＋ 3）、<b>倍數</b>（○ ＝ □ × 4），或<b>倍數再加</b>（○ ＝ □ × 2 ＋ 1）。",
         "有了關係式，就能算出任何 □ 對應的 ○，也能反過來求 □。"],
        [example("□：1、2、3、4；○：3、5、7、9。關係式？", ["□ 每多 1，○ 就多 2。", "□ × 2 再加 1：1 × 2 ＋ 1 ＝ 3。"], "○ ＝ □ × 2 ＋ 1"),
         example("排三角形：1 個 3 根，每多 1 個多 2 根。10 個幾根？", ["○ ＝ □ × 2 ＋ 1。", "10 × 2 ＋ 1 ＝ 21。"], "21 根")],
        [("只看第一組就寫關係式", "每一組都要檢查"),
         ("○ ＝ □ × 2 ＋ 1 寫成 ○ ＝ □ × 3", "代 □ ＝ 2 檢查：5 不是 6"),
         ("連在一起的三角形，每個都算 3 根", "共用的邊只算一次：每多 1 個多 2 根")])
    faq = [{"q": "怎麼從表格找出關係式？",
            "a": "先看 □ 每多 1，○ 多多少；再看和、差、倍數是不是固定。找到後用每一組數字代進去檢查。"},
           {"q": "關係式有什麼用？",
            "a": "不用把表格一直寫下去，就能直接算出第 100 個是多少；這是國中代數和函數的前置經驗。"},
           {"q": "六年級的數量關係要學什麼？",
            "a": "108課綱 R-6-2、R-6-3：從具體情境或數量模式出發，觀察、推理、說明，並用文字或符號列出數量關係的關係式。"}]
    make_unit(R, "grade-6", "quantity-relationships", "R-6-3",
              "數量關係的表示：代數與函數的前置經驗。將具體情境或模式中的數量關係，學習以文字或符號列出數量關係的關係式。",
              "數量關係與關係式",
              "六年級數學 數量關係 練習題｜表格規律・關係式・火柴棒 學習單（附解答）",
              "數量關係",
              "國小六年級數學「數量關係與關係式」免費學習單：找出表格的規律、用 □ 和 ○ 寫出關係式、把情境寫成關係式、火柴棒和排桌子的圖形模式與用關係式求值。100題線上練習馬上對答案，附可列印解答。",
              "用 □ 和 ○ 寫出兩個量的關係",
              "看表時每一組都要檢查：和、差、倍數還是倍數再加。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
