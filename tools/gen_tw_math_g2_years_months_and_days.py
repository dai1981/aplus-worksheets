# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：年、月、星期、日（108課綱 N-2-14）
  python3 tools/gen_tw_math_g2_years_months_and_days.py
1 年 ＝ 12 個月、1 星期 ＝ 7 天、大月（31 天）と小月（30 天）と 2 月、幾個星期は幾天、同じ月の日數の差、月曆で何曜日、生活の場面。
誤答：大月と小月の取り違え、日數の差で「両端を含める」かどうかを間違える、星期を 5 天とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, line, INK, GREEN, RED
from tw_g7 import tidy_sets

R = random.Random(81315)
NM = Names(R)
WK = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def cal(m, start):
    W, cw, ch = 7 * 40 + 10, 40, 30
    rows = (start + DAYS[m - 1] + 6) // 7
    s = [text(W / 2, 20, "%d 月" % m, 16, col=GREEN)]
    for i, w in enumerate("日一二三四五六"):
        s.append(text(5 + cw * i + cw / 2, 46, w, 13, col=RED if i in (0, 6) else INK))
    for d in range(1, DAYS[m - 1] + 1):
        r, c = divmod(start + d - 1, 7)
        s.append(text(5 + cw * c + cw / 2, 72 + r * ch, str(d), 13, col=RED if c in (0, 6) else INK, weight=400))
    s.append(line(5, 54, W - 5, 54, GREEN, 1.2))
    return fig(svg_wrap(W, 64 + rows * ch, "".join(s), "%d 月月曆" % m).replace("<svg ", "<svg data-pf='lg' ", 1))


def s1(seen):
    out = []
    for m in range(1, 13):
        d = DAYS[m - 1]
        if m == 2:
            out.append(mcq("2 月通常有幾天？", "28 天（有些年 29 天）", ["30 天", "31 天", "27 天"], "2 月最特別，平常 28 天，閏年 29 天。"))
            continue
        out.append(mcq("%d 月有幾天？" % m, "%d 天" % d, ["%d 天" % x for x in (61 - d, 28, 29)], "%d 月是%s，有 %d 天。" % (m, "大月" if d == 31 else "小月", d)))
    FACTS = [("一年有幾個月？", "12 個月", ["10 個月", "7 個月", "52 個月"], "1 月到 12 月，一年有 12 個月。"),
             ("一個星期有幾天？", "7 天", ["5 天", "6 天", "10 天"], "星期日到星期六，共 7 天。"),
             ("一年中，有 31 天的「大月」有幾個？", "7 個", ["6 個", "5 個", "12 個"], "1、3、5、7、8、10、12 月，共 7 個大月。"),
             ("一年中，有 30 天的「小月」有幾個？", "4 個", ["5 個", "6 個", "7 個"], "4、6、9、11 月，共 4 個小月（2 月另外算）。"),
             ("7 月和 8 月都是大月嗎？", "都是大月，各 31 天", ["7 月大、8 月小", "7 月小、8 月大", "都是小月"], "7 月和 8 月連續兩個大月。"),
             ("12 月 31 日的下一天是哪一天？", "1 月 1 日", ["12 月 32 日", "13 月 1 日", "11 月 1 日"], "12 月 31 日是一年的最後一天，下一天是新的一年 1 月 1 日。"),
             ("4 月 30 日的下一天是哪一天？", "5 月 1 日", ["4 月 31 日", "5 月 30 日", "4 月 1 日"], "4 月是小月只有 30 天，下一天是 5 月 1 日。"),
             ("用拳頭記大小月，凸起來的（骨頭）是什麼月？", "大月（31 天）", ["小月（30 天）", "2 月", "沒有關係"], "拳頭上凸起的是大月，凹下的是小月（2 月除外）。")]
    out += [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])
    return out


def s2(seen):
    def mk():
        k = R.choice(["w2d", "d2w", "mix", "y2m"])
        if k == "w2d":
            w = R.randint(2, 9)
            q = "%d 個星期是幾天？" % w
            return mcq(q, "%d 天" % (7 * w), ["%d 天" % x for x in (5 * w, 7 * w + 7, w + 7)], "1 星期 ＝ 7 天，7 × %d ＝ %d。" % (w, 7 * w))
        if k == "d2w":
            w = R.randint(2, 9)
            q = "%d 天是幾個星期？" % (7 * w)
            return mcq(q, "%d 個星期" % w, ["%d 個星期" % x for x in (w + 1, w - 1, 7 * w // 5 if 7 * w % 5 == 0 else w + 2)], "7 × %d ＝ %d，是 %d 個星期。" % (w, 7 * w, w))
        if k == "mix":
            w, d = R.randint(1, 4), R.randint(1, 6)
            q = "%d 個星期又 %d 天，一共是幾天？" % (w, d)
            return mcq(q, "%d 天" % (7 * w + d), ["%d 天" % x for x in (w + d, 7 * w, 10 * w + d)], "7 × %d ＝ %d，%d ＋ %d ＝ %d。" % (w, 7 * w, 7 * w, d, 7 * w + d))
        y = R.randint(2, 5)
        q = "%d 年是幾個月？" % y
        return mcq(q, "%d 個月" % (12 * y), ["%d 個月" % x for x in (10 * y, 12 * y + 12, y + 12)], "1 年 ＝ 12 個月，12 × %d ＝ %d。" % (y, 12 * y))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        m = R.randint(1, 12)
        start = R.randrange(7)
        d = R.randint(1, DAYS[m - 1])
        k = R.choice(["weekday", "count"])
        if k == "weekday":
            v = WK[(start + d - 1) % 7]
            q = "看月曆，%d 月 %d 日是星期幾？" % (m, d) + cal(m, start)
            return mcq(q, v, [WK[(start + d) % 7], WK[(start + d - 2) % 7], WK[(start + d + 2) % 7]], "找到 %d 日，往上看是「%s」。" % (d, v[-1]))
        wd = R.randrange(7)
        n = sum(1 for x in range(1, DAYS[m - 1] + 1) if (start + x - 1) % 7 == wd)
        q = "看月曆，%d 月有幾個%s？" % (m, WK[wd]) + cal(m, start)
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (4, 5, 3, 6) if x != n][:3], "在「%s」那一行數一數，有 %d 個。" % (WK[wd][-1], n))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        m = R.randint(1, 12)
        a, b = sorted(R.sample(range(1, DAYS[m - 1] + 1), 2))
        k = R.choice(["after", "between"])
        if k == "after":
            n = b - a
            q = "今天是 %d 月 %d 日，再過幾天是 %d 月 %d 日？" % (m, a, m, b)
            return mcq(q, "%d 天" % n, ["%d 天" % x for x in (n + 1, n - 1 if n > 1 else n + 2, a + b)], "%d － %d ＝ %d 天。" % (b, a, n))
        n = b - a + 1
        q = "%d 月 %d 日到 %d 月 %d 日舉辦書展（兩天都有展），一共展了幾天？" % (m, a, m, b)
        return mcq(q, "%d 天" % n, ["%d 天" % x for x in (n - 1, n + 1, a + b)], "%d － %d ＝ %d，頭尾兩天都要算，再加 1：%d 天。" % (b, a, b - a, n))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        who = NM.next()
        k = R.choice(["after_week", "age", "month_after"])
        if k == "after_week":
            m = R.randint(1, 12)
            d = R.randint(1, DAYS[m - 1] - 7)
            w = R.randrange(7)
            q = "%d 月 %d 日是%s，下一個%s是幾月幾日？" % (m, d, WK[w], WK[w])
            return mcq(q, "%d 月 %d 日" % (m, d + 7), ["%d 月 %d 日" % (m, x) for x in (d + 1, d + 6, d + 8)], "一個星期 7 天：%d ＋ 7 ＝ %d。" % (d, d + 7))
        if k == "age":
            a = R.randint(6, 9)
            b = R.randint(1, 4)
            q = "%s今年 %d 歲，%d 年後是幾歲？" % (who, a, b)
            return mcq(q, "%d 歲" % (a + b), ["%d 歲" % x for x in (a + b + 1, a - b, a + 12 * b)], "每過 1 年長 1 歲：%d ＋ %d ＝ %d。" % (a, b, a + b))
        m = R.randint(1, 12)
        k2 = R.randint(2, 6)
        v = (m + k2 - 1) % 12 + 1
        q = "現在是 %d 月，再過 %d 個月是幾月？" % (m, k2)
        return mcq(q, "%d 月" % v, ["%d 月" % x for x in ((m + k2) if m + k2 > 12 else v + 1, v - 1 if v > 1 else 12, (v % 12) + 1) if x != v][:3] + ["%d 月" % ((v + 2) % 12 + 1)], "%d 月往後數 %d 個月是 %d 月%s。" % (m, k2, v, "（過了 12 月要從 1 月開始）" if m + k2 > 12 else ""))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("大月和小月", s1(seen)), ("年、月、星期、日的換算", s2(seen)), ("看月曆", s3(seen)),
            ("過了幾天", s4(seen)), ("生活中的日期", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>1 年 ＝ 12 個月</b>，<b>1 星期 ＝ 7 天</b>。",
         "<b>大月</b> 31 天：1、3、5、7、8、10、12 月；<b>小月</b> 30 天：4、6、9、11 月；2 月平常 28 天。",
         "算「再過幾天」用後面的日期 － 前面的日期；算「從哪天到哪天共幾天」（頭尾都算）要再加 1。" + cal(5, 3)],
        [example("3 個星期又 2 天", ["7 × 3 ＝ 21。", "21 ＋ 2。"], "23 天"),
         example("5 月 8 日到 5 月 12 日（頭尾都算）", ["12 － 8 ＝ 4，再加 1。"], "5 天")],
        [("6 月有 31 天", "6 月是小月，30 天"),
         ("8 日到 12 日共 4 天", "頭尾都算是 5 天"),
         ("1 個星期 5 天", "上學 5 天，但一星期有 7 天")])
    faq = [{"q": "二年級要學哪些時間單位？",
            "a": "108課綱 N-2-14：年、月、星期、日，理解它們之間的關係，並會看月曆。"},
           {"q": "大月小月怎麼記？",
            "a": "用拳頭數：從食指的關節開始，凸起來是大月、凹下去是小月，數到 7 月後再從頭數 8 月。"},
           {"q": "為什麼「頭尾都算」要加 1？",
            "a": "例如 8 日到 12 日：8、9、10、11、12，共 5 天；相減得到的 4 是「過了幾天」。"}]
    make_unit(R, "grade-2", "years-months-and-days", "N-2-14",
              "時間：「年」、「月」、「星期」、「日」。理解所列時間單位之間的關係。",
              "年、月、星期、日",
              "二年級數學 年月日 練習題｜大月小月・月曆・星期換算 學習單（附解答）",
              "年、月、星期、日",
              "國小二年級數學「年、月、星期、日」免費學習單：大月和小月、年月星期日的換算、看月曆、過了幾天和頭尾都算、生活中的日期。100題線上練習，附可列印解答。",
              "1 年 12 個月，1 星期 7 天",
              "大月 31 天、小月 30 天、2 月 28 天。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
