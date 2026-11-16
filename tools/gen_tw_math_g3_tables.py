# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：一維表格與二維表格（108課綱 D-3-1）
  python3 tools/gen_tw_math_g3_tables.py
一維表格の報讀と計算、二維表格（列聯表）の報讀、合計欄と空欄の計算、「正」字記錄から表を作る。
誤答：行と列を取り違える、合計欄を足し忘れる・二重に数える、正 1 つを 1 と数える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table

R = random.Random(31021)
NM = Names(R)

THEMES = [("最喜歡的水果", ["蘋果", "香蕉", "芒果", "西瓜", "葡萄"], "人"),
          ("最喜歡的運動", ["跳繩", "籃球", "游泳", "躲避球", "羽球"], "人"),
          ("上學的方式", ["走路", "騎腳踏車", "坐公車", "家長接送", "搭捷運"], "人"),
          ("圖書館借出的書", ["故事書", "科學書", "漫畫", "繪本", "百科"], "本"),
          ("文具店賣出的文具", ["鉛筆", "橡皮擦", "尺", "筆記本", "色筆"], "個")]
DAYS = ["星期一", "星期二", "星期三", "星期四", "星期五"]


def one_table():
    title, cats, u = R.choice(THEMES)
    k = R.randint(4, 5)
    cs = cats[:k]
    vals = R.sample(range(3, 19), k)
    return title, cs, vals, u


def tbl1(title, cs, vals, u):
    return "<p>%s</p>" % title + table(["項目"] + cs, [["%s（%s）" % ("人數" if u == "人" else "數量", u)] + [str(v) for v in vals]])


def s1(seen):
    def mk():
        title, cs, vals, u = one_table()
        kind = R.choice(["most", "least", "look"])
        q0 = "看表格回答。" + tbl1(title, cs, vals, u)
        if kind == "most":
            ans = cs[vals.index(max(vals))]
            return mcq(q0 + "哪一項最多？", ans, [c for c in cs if c != ans], "%s有 %d %s，是最多的。" % (ans, max(vals), u))
        if kind == "least":
            ans = cs[vals.index(min(vals))]
            return mcq(q0 + "哪一項最少？", ans, [c for c in cs if c != ans], "%s只有 %d %s，是最少的。" % (ans, min(vals), u))
        i = R.randrange(len(cs))
        return mcq(q0 + "%s有幾%s？" % (cs[i], u), "%d %s" % (vals[i], u), ["%d %s" % (v, u) for v in vals if v != vals[i]] + ["%d %s" % (vals[i] + 1, u)],
                   "找到「%s」那一格：%d %s。" % (cs[i], vals[i], u))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        title, cs, vals, u = one_table()
        kind = R.choice(["sum", "diff", "two"])
        q0 = "看表格回答。" + tbl1(title, cs, vals, u)
        if kind == "sum":
            t = sum(vals)
            return mcq(q0 + "一共有幾%s？" % u, "%d %s" % (t, u), ["%d %s" % (x, u) for x in (t - vals[-1], t + vals[0], t - 1, max(vals) * len(vals))],
                       "全部加起來：%s ＝ %d（%s）。" % (" ＋ ".join(map(str, vals)), t, u))
        if kind == "diff":
            i, j = R.sample(range(len(cs)), 2)
            if vals[i] < vals[j]:
                i, j = j, i
            d = vals[i] - vals[j]
            return mcq(q0 + "%s比%s多幾%s？" % (cs[i], cs[j], u), "%d %s" % (d, u), ["%d %s" % (x, u) for x in (vals[i] + vals[j], vals[i], d + 1, d + 2)],
                       "%d － %d ＝ %d（%s）。" % (vals[i], vals[j], d, u))
        i, j = R.sample(range(len(cs)), 2)
        s = vals[i] + vals[j]
        return mcq(q0 + "%s和%s合起來有幾%s？" % (cs[i], cs[j], u), "%d %s" % (s, u), ["%d %s" % (x, u) for x in (abs(vals[i] - vals[j]), s + 1, s - 1, s + 10)],
                   "%d ＋ %d ＝ %d（%s）。" % (vals[i], vals[j], s, u))
    return pick_unique(R, mk, 20, seen)


def two_table(total=False):
    title, cats, u = R.choice(THEMES[:3])
    k = R.randint(3, 4)
    cs = cats[:k]
    rows = [("男生", [R.randint(2, 12) for _ in cs]), ("女生", [R.randint(2, 12) for _ in cs])]
    if R.random() < .4:
        rows = [("三年甲班", rows[0][1]), ("三年乙班", rows[1][1])]
    head = ["%s＼%s" % ("班級" if "班" in rows[0][0] else "性別", title)] + cs + (["合計"] if total else [])
    body = []
    for name, v in rows:
        body.append([name] + [str(x) for x in v] + ([str(sum(v))] if total else []))
    if total:
        cols = [rows[0][1][i] + rows[1][1][i] for i in range(k)]
        body.append(["合計"] + [str(c) for c in cols] + [str(sum(cols))])
    return title, cs, rows, u, head, body


def s3(seen):
    def mk():
        title, cs, rows, u, head, body = two_table()
        q0 = "看二維表格回答。<p>%s（單位：%s）</p>" % (title, u) + table(head, body)
        r = R.randrange(2)
        i = R.randrange(len(cs))
        v = rows[r][1][i]
        other = rows[1 - r][1][i]
        kind = R.choice(["cell", "cell", "most"])
        if kind == "cell":
            w = [x for x in [other] + rows[r][1] + [v + 1, v + 2] if x != v]
            return mcq(q0 + "%s%s的有幾%s？" % (rows[r][0], ("喜歡" + cs[i]) if "喜歡" in title else cs[i], u), "%d %s" % (v, u), ["%d %s" % (x, u) for x in w],
                       "找「%s」那一列和「%s」那一行交會的格子：%d。" % (rows[r][0], cs[i], v))
        vals = rows[r][1]
        if vals.count(max(vals)) > 1:
            return None
        ans = cs[vals.index(max(vals))]
        return mcq(q0 + "%s中，哪一項最多？" % rows[r][0], ans, [c for c in cs if c != ans] + ["一樣多"],
                   "只看「%s」那一列：%s最多（%d）。" % (rows[r][0], ans, max(vals)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        title, cs, rows, u, head, body = two_table(total=True)
        k = len(cs)
        kind = R.choice(["miss", "rowtot", "coltot", "grand"])
        if kind == "miss":
            r, i = R.randrange(2), R.randrange(k)
            v = rows[r][1][i]
            body = [list(x) for x in body]
            body[r][1 + i] = "？"
            q = "表格裡「？」是多少？<p>%s（單位：%s）</p>" % (title, u) + table(head, body)
            col_tot = rows[0][1][i] + rows[1][1][i]
            row_tot = sum(rows[r][1])
            return mcq(q, str(v), [str(x) for x in (col_tot, row_tot - v if row_tot - v != v else v + 3, v + 1, col_tot + v)],
                       "看「%s」那一行：合計 %d － %d ＝ %d。（也可以用那一列的合計來算）" % (cs[i], col_tot, rows[1 - r][1][i], v))
        if kind == "rowtot":
            r = R.randrange(2)
            body2 = [list(x) for x in body]
            body2[r][-1] = "？"
            t = sum(rows[r][1])
            q = "表格裡「？」是多少？<p>%s（單位：%s）</p>" % (title, u) + table(head, body2)
            return mcq(q, str(t), [str(x) for x in (t - rows[r][1][-1], sum(rows[1 - r][1]), t + 1, t * 2)], "把「%s」那一列加起來：%s ＝ %d。" % (rows[r][0], " ＋ ".join(map(str, rows[r][1])), t))
        if kind == "coltot":
            i = R.randrange(k)
            body2 = [list(x) for x in body]
            body2[2][1 + i] = "？"
            t = rows[0][1][i] + rows[1][1][i]
            q = "表格裡「？」是多少？<p>%s（單位：%s）</p>" % (title, u) + table(head, body2)
            return mcq(q, str(t), [str(x) for x in (abs(rows[0][1][i] - rows[1][1][i]), t + 1, t - 1, rows[0][1][i])], "把「%s」那一行加起來：%d ＋ %d ＝ %d。" % (cs[i], rows[0][1][i], rows[1][1][i], t))
        body2 = [list(x) for x in body]
        body2[2][-1] = "？"
        t = sum(rows[0][1]) + sum(rows[1][1])
        q = "表格右下角的「？」是多少？<p>%s（單位：%s）</p>" % (title, u) + table(head, body2)
        return mcq(q, str(t), [str(x) for x in (sum(rows[0][1]), t * 2, t + 1, t - 2)], "右下角是全部的總數：%d ＋ %d ＝ %d。" % (sum(rows[0][1]), sum(rows[1][1]), t))
    return pick_unique(R, mk, 20, seen)


def zheng(n):
    """「正」字記錄：5 ごとに 正、残りは 一 丅 下 止"""
    part = ["", "一", "丅", "下", "止"]
    return "正" * (n // 5) + part[n % 5]


def s5(seen):
    def count():
        n = R.randint(6, 23)
        if n % 5 == 0 and R.random() < .5:
            return None
        q = "用畫「正」字的方法記錄，「%s」代表幾？" % zheng(n)
        return mcq(q, str(n), [str(x) for x in (n // 5 + n % 5, n + 1, n - 1, (n // 5) * 10 + n % 5)],
                   "一個「正」是 5 筆，代表 5。%d 個正是 %d%s，共 %d。" % (n // 5, n // 5 * 5, "，再加 %d" % (n % 5) if n % 5 else "", n))

    def make():
        title, cs, vals, u = one_table()
        cs, vals = cs[:3], vals[:3]
        rec = "；".join("%s：%s" % (c, zheng(v)) for c, v in zip(cs, vals))
        i = R.randrange(3)
        q = "用「正」字記錄%s：%s。做成表格時，%s要填多少？" % (title, rec, cs[i])
        v = vals[i]
        return mcq(q, str(v), [str(x) for x in (v // 5 + v % 5, v + 5, v - 1, len(zheng(v)))],
                   "%s是「%s」：%d 個正（%d），再加 %d 筆，共 %d。" % (cs[i], zheng(v), v // 5, v // 5 * 5, v % 5, v))

    def plan():
        who = NM.next()
        days = R.sample(DAYS, 5)
        vals = [R.randint(2, 9) for _ in DAYS]
        q = "%s記錄一週每天看書的時間（分鐘）：" % who + table(["星期"] + DAYS, [["時間（分鐘）"] + [str(v * 5) for v in vals]]) + "看書時間超過 30 分鐘的有幾天？"
        n = sum(1 for v in vals if v * 5 > 30)
        if n == 0:
            return None
        return mcq(q, "%d 天" % n, ["%d 天" % x for x in range(0, 6) if x != n][:3] + ["%d 天" % (n + 2)],
                   "超過 30 分鐘（不含 30）的有：%s，共 %d 天。" % ("、".join(DAYS[i] for i, v in enumerate(vals) if v * 5 > 30), n))
    return pick_unique(R, count, 8, seen) + pick_unique(R, make, 6, seen) + pick_unique(R, plan, 6, seen)


def main():
    seen = set()
    sets = [("讀一維表格", s1(seen)), ("一維表格的計算", s2(seen)), ("讀二維表格", s3(seen)),
            ("二維表格的合計", s4(seen)), ("畫正字和做表格", s5(seen))]
    demo = table(["性別＼最喜歡的水果", "蘋果", "香蕉", "芒果", "合計"],
                 [["男生", "5", "3", "6", "14"], ["女生", "4", "7", "2", "13"], ["合計", "9", "10", "8", "27"]])
    body = lesson(
        ["<b>一維表格</b>只有一種分類，例如「最喜歡的水果」各有幾人。",
         "<b>二維表格</b>有兩種分類：橫的叫<b>列</b>，直的叫<b>行</b>。找資料時，看列和行交會的那一格。",
         "<b>合計</b>：最右邊一行是每一列加起來，最下面一列是每一行加起來，右下角是全部的總數。",
         "記錄資料時常畫「正」字：一個「正」是 5 筆。"],
        [example("喜歡香蕉的女生有幾人？" + demo, ["找「女生」那一列和「香蕉」那一行交會的格子。"], "7 人"),
         example("喜歡芒果的一共有幾人？", ["看「芒果」那一行：6 ＋ 2 ＝ 8，也可以直接看合計那一列。"], "8 人")],
        [("看錯列和行，找到旁邊的格子", "用手指一個沿著列、一個沿著行，在交會處停下來"),
         ("把合計也加進去，算出兩倍的總數", "總數只加資料格，或直接看右下角"),
         ("「正」只算 1", "一個「正」有 5 筆，代表 5")])
    faq = [{"q": "一維表格和二維表格有什麼不同？",
            "a": "一維表格只依一種分類整理（例如水果種類）；二維表格同時依兩種分類整理（例如性別和水果種類），也叫列聯表。"},
           {"q": "三年級的表格單元要學什麼？",
            "a": "108課綱 D-3-1：報讀、說明和製作生活中的一維、二維表格，包含有合計的列聯表。長條圖在四年級學。"},
           {"q": "為什麼要用「正」字記錄？",
            "a": "「正」有 5 筆，每 5 個湊成一個「正」，數的時候 5 個 5 個數，又快又不容易數錯。"}]
    make_unit(R, "grade-3", "tables", "D-3-1",
              "一維表格與二維表格：以操作活動為主。報讀、說明與製作生活中的表格。二維表格含列聯表。",
              "一維表格與二維表格：報讀和製作",
              "三年級數學 表格 練習題｜一維表格・二維表格・列聯表 學習單（附解答）",
              "一維和二維表格",
              "國小三年級數學「表格」免費學習單：讀一維表格和二維表格、找列和行交會的格子、算合計、用「正」字記錄做表格。100題線上練習馬上對答案，附可列印解答。",
              "二維表格：找列和行交會的那一格",
              "最右邊是每一列的合計，最下面是每一行的合計。",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
