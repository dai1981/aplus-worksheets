# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：日期與時間（108課綱 N-1-6）
  python3 tools/gen_tw_math_g1_dates_and_time.py
今天・昨天・明天、星期の順序、幾月幾日の報讀（月曆）、上午・中午・下午・晚上、鐘面の整點と半點。
誤答：昨天と明天の取り違え、長針と短針の取り違え（3 時 → 12 時 15 分）、半點で短針の位置を前の數字にしない。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, clock, fig, svg_wrap, text, line, INK, GREEN, RED
from tw_g7 import tidy_sets

R = random.Random(81210)
WK = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def s1(seen):
    def mk():
        i = R.randrange(7)
        k = R.choice(["明天", "昨天", "後天", "前天"])
        d = {"明天": 1, "昨天": -1, "後天": 2, "前天": -2}[k]
        v = WK[(i + d) % 7]
        q = "今天是%s，%s是星期幾？" % (WK[i], k)
        w = [WK[(i - d) % 7], WK[i], WK[(i + d + (1 if d > 0 else -1)) % 7]]
        return mcq(q, v, w, "%s是往%s數 %d 天：%s。" % (k, "後" if d > 0 else "前", abs(d), v))
    return pick_unique(R, mk, 20, seen)


def cal(m, start):
    """m 月の月曆（start：1 日の曜日 0＝日）"""
    W, cw, ch = 7 * 40 + 10, 40, 30
    rows = (start + DAYS[m - 1] + 6) // 7
    s = [text(W / 2, 20, "%d 月" % m, 16, col=GREEN)]
    for i, w in enumerate("日一二三四五六"):
        s.append(text(5 + cw * i + cw / 2, 46, w, 13, col=RED if i in (0, 6) else INK))
    for d in range(1, DAYS[m - 1] + 1):
        k = start + d - 1
        r, c = divmod(k, 7)
        s.append(text(5 + cw * c + cw / 2, 72 + r * ch, str(d), 13, col=RED if c in (0, 6) else INK, weight=400))
    s.append(line(5, 54, W - 5, 54, GREEN, 1.2))
    return fig(svg_wrap(W, 64 + rows * ch, "".join(s), "%d 月月曆" % m).replace("<svg ", "<svg data-pf='lg' ", 1))


def s2(seen):
    def mk():
        m = R.randint(1, 12)
        start = R.randrange(7)
        d = R.randint(1, DAYS[m - 1])
        k = R.choice(["weekday", "next"])
        if k == "weekday":
            v = WK[(start + d - 1) % 7]
            q = "看月曆，%d 月 %d 日是星期幾？" % (m, d) + cal(m, start)
            return mcq(q, v, [WK[(start + d) % 7], WK[(start + d - 2) % 7], WK[(start + d + 2) % 7]], "找到 %d 日，往上看是「%s」。" % (d, v[-1]))
        if d + 7 > DAYS[m - 1]:
            return None
        q = "看月曆，%d 月 %d 日的下一個星期同一天是幾月幾日？" % (m, d) + cal(m, start)
        return mcq(q, "%d 月 %d 日" % (m, d + 7), ["%d 月 %d 日" % (m, x) for x in (d + 1, d + 6, d + 8)], "一個星期有 7 天：%d ＋ 7 ＝ %d。" % (d, d + 7))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    EV = [("起床吃早餐", "上午"), ("升旗典禮", "上午"), ("吃午餐", "中午"), ("午休", "中午"), ("放學回家", "下午"), ("上體育課（第六節）", "下午"),
          ("吃晚餐", "晚上"), ("洗澡睡覺", "晚上"), ("看星星", "晚上"), ("去上學", "上午"), ("下午茶點心", "下午"), ("看月亮", "晚上")]
    out = []
    for e, t in EV:
        out.append(mcq("「%s」通常是在什麼時候？" % e, t, [x for x in ["上午", "中午", "下午", "晚上"] if x != t], "%s通常在%s。" % (e, t)))
    FACTS = [("一個星期有幾天？", "7 天", ["5 天", "10 天", "12 天"], "星期日到星期六，共 7 天。"),
             ("一年有幾個月？", "12 個月", ["10 個月", "7 個月", "30 個月"], "1 月到 12 月，共 12 個月。"),
             ("星期六的下一天是星期幾？", "星期日", ["星期一", "星期五", "星期七"], "星期六過完是星期日，沒有星期七。"),
             ("12 月的下一個月是幾月？", "1 月", ["13 月", "11 月", "2 月"], "12 月過完是新的一年的 1 月。"),
             ("今天是 5 月 10 日，明天是幾月幾日？", "5 月 11 日", ["5 月 9 日", "6 月 10 日", "5 月 12 日"], "明天多 1 天：11 日。"),
             ("今天是 3 月 1 日，昨天是哪一個月？", "2 月", ["3 月", "4 月", "1 月"], "3 月 1 日的前一天是 2 月的最後一天。"),
             ("中午大約是幾時？", "12 時", ["6 時", "9 時", "3 時"], "中午大約是 12 時。"),
             ("太陽下山以後是什麼時候？", "晚上", ["上午", "中午", "下午"], "太陽下山就是晚上了。")]
    out += [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])
    return out


def s4(seen):
    def mk():
        h = R.randint(1, 12)
        half = R.random() < .5
        m = 30 if half else 0
        q = "鐘面上是幾時幾分？" + clock(h, m, 170)
        ans = "%d 時%s" % (h, " 30 分" if half else "")
        if half:
            w = ["%d 時 30 分" % (h % 12 + 1), "%d 時" % h, "6 時 %d 分" % (h * 5) if h * 5 < 60 else "%d 時 6 分" % h]
        else:
            w = ["12 時 %d 分" % (h * 5) if h != 12 else "12 時 30 分", "%d 時 30 分" % h, "%d 時" % (h % 12 + 1)]
        e = ("長針指著 12，短針指著 %d：%d 時。" % (h, h)) if not half else "長針指著 6 是 30 分，短針在 %d 和 %d 中間：%d 時 30 分（也叫 %d 時半）。" % (h, h % 12 + 1, h, h)
        return mcq(q, ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        h = R.randint(7, 11)
        half = R.random() < .5
        ev = "出門上學" if h == 7 else "上第一節課" if h == 8 else R.choice(["星期六出門去公園", "星期日開始寫功課", "星期六去圖書館"])
        q = "%s的時候，鐘面是這樣。是上午幾時幾分？" % ev + clock(h, 30 if half else 0, 170)
        ans = "上午 %d 時%s" % (h, " 30 分" if half else "")
        return mcq(q, ans, ["下午 %d 時%s" % (h, " 30 分" if half else ""), "上午 %d 時%s" % (h + 1, " 30 分" if half else ""), "上午 12 時 %d 分" % (h * 5)], "%s是在早上，所以是上午；%s。" % (ev, "長針指 6，短針在 %d 和 %d 中間" % (h, h + 1) if half else "長針指 12，短針指 %d" % h))

    def later():
        h = R.randint(1, 10)
        k = R.choice([1, 2])
        q = "現在是 %d 時。再過 %d 小時是幾時？" % (h, k)
        return mcq(q, "%d 時" % (h + k), ["%d 時" % x for x in (h - k if h - k > 0 else h + k + 1, h + k + 1, h)], "%d ＋ %d ＝ %d。" % (h, k, h + k))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, later, 8, seen)


def main():
    seen = set()
    sets = [("昨天、今天、明天", s1(seen)), ("看月曆", s2(seen)), ("上午、中午、下午、晚上", s3(seen)),
            ("整點和半點", s4(seen)), ("生活中的時間", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["今天的前一天是<b>昨天</b>，後一天是<b>明天</b>。一個星期有 7 天，一年有 12 個月。",
         "看<b>月曆</b>：先找日期，再往上看是星期幾。",
         "<b>整點</b>：長針指著 12，短針指幾就是幾時。<b>半點</b>：長針指著 6，是幾時 30 分，短針在兩個數字中間。" + clock(3, 0, 150) + clock(3, 30, 150)],
        [example("今天星期五，明天星期幾？", ["往後數 1 天。"], "星期六"),
         example("長針指 6，短針在 8 和 9 中間", ["是 8 時 30 分。"], "8 時 30 分")],
        [("長針指 3、短針指 12，讀成 3 時", "看短針：12 時 15 分；整點時長針指 12"),
         ("8 時 30 分時，讀成 9 時 30 分", "短針還沒到 9，是 8 時 30 分"),
         ("星期六的下一天是星期七", "是星期日")])
    faq = [{"q": "一年級要會看到幾分？",
            "a": "108課綱 N-1-6：一年級學日期（幾月幾日）、昨天今天明天、上午中午下午晚上，鐘面先認識整點和半點，二年級再學幾時幾分。"},
           {"q": "怎麼分長針和短針？",
            "a": "短針（時針）比較短、走得慢，告訴我們幾時；長針（分針）比較長，告訴我們幾分。"},
           {"q": "怎麼在家練習？",
            "a": "每天起床、吃飯、睡覺時一起看時鐘說「現在是幾時」，再看月曆說「今天幾月幾日星期幾」。"}]
    make_unit(R, "grade-1", "dates-and-time", "N-1-6",
              "日常時間用語：以操作活動為主。簡單日期報讀「幾月幾日」；「明天」、「今天」、「昨天」；「上午」、「中午」、「下午」、「晚上」。",
              "日期與時間：月曆和整點、半點",
              "一年級數學 時間 練習題｜昨天今天明天・月曆・整點半點 學習單（附解答）",
              "日期與時間",
              "國小一年級數學「日期與時間」免費學習單：昨天今天明天和星期、看月曆、上午中午下午晚上、鐘面的整點和半點、生活中的時間。100題線上練習，題目短、圖多，附可列印解答。",
              "整點長針指 12，半點長針指 6",
              "短針指幾就是幾時；半點時短針在兩個數字中間。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
