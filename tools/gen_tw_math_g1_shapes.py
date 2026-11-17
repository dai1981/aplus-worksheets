# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：認識形狀（108課綱 S-1-1、S-1-2）
  python3 tools/gen_tw_math_g1_shapes.py
平面圖形の名前（三角形・正方形・長方形・圓形）、圖形を數える、邊と角（頂點）の數、立體（球・正方體・圓柱・圓錐）の名前と性質（滾動・堆疊）、生活の中の形。
誤答：正方形と長方形の取り違え、向きが變わると別の形と思う、圓に角があるとする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81211)
SH = {"triangle": "三角形", "square": "正方形", "rectangle": "長方形", "circle": "圓形"}
SO = {"sphere": "球", "cube": "正方體", "cylinder": "圓柱", "cone": "圓錐"}
COL = ["red", "blue", "yellow", "green"]


def s1(seen):
    def mk():
        k = R.choice(list(SH))
        c = R.choice(COL)
        size = R.choice([24, 30, 36])
        q = "這是什麼形狀？" + P.shapes_row([(k, c)], size=size)
        return mcq(q, SH[k], [v for x, v in SH.items() if x != k], {"triangle": "有 3 條邊、3 個角，是三角形。", "square": "4 條邊一樣長、4 個角都是直角，是正方形。", "rectangle": "4 個角都是直角，長邊和短邊不一樣長，是長方形。", "circle": "圓圓的，沒有邊也沒有角，是圓形。"}[k])
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(5, 7)
        items = [(R.choice(list(SH)), R.choice(COL)) for _ in range(n)]
        k = R.choice(list(SH))
        c = sum(1 for x, _ in items if x == k)
        q = "下面有幾個%s？" % SH[k] + P.shapes_row(items, size=22)
        return mcq(q, "%d 個" % c, ["%d 個" % x for x in (c + 1, c - 1 if c > 0 else c + 2, n) if x != c][:3] + ["%d 個" % (c + 2)], "一個一個找%s，共 %d 個。" % (SH[k], c))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice(["triangle", "square", "rectangle", "circle"])
        what = R.choice(["邊", "角"])
        v = {"triangle": 3, "square": 4, "rectangle": 4, "circle": 0}[k]
        q = "%s有幾個%s？" % (SH[k], what) + P.shapes_row([(k, R.choice(COL))], size=30)
        return mcq(q, "%d 個" % v if v else "沒有%s" % what, ["%d 個" % x for x in (3, 4, 5, 1) if x != v][:3], ("%s有 %d 條邊、%d 個角。" % (SH[k], v, v)) if v else "圓形沒有直直的邊，也沒有角。")

    FACTS = [("哪一個形狀沒有角？", "圓形", ["三角形", "正方形", "長方形"], "圓形是圓圓的，沒有角。"),
             ("哪一個形狀只有 3 條邊？", "三角形", ["正方形", "長方形", "圓形"], "三角形有 3 條邊。"),
             ("正方形的 4 條邊怎麼樣？", "一樣長", ["都不一樣長", "只有 2 條一樣長", "沒有邊"], "正方形 4 條邊一樣長。"),
             ("把三角形轉一轉，它還是三角形嗎？", "還是三角形", ["變成正方形", "變成圓形", "不是形狀了"], "轉方向不會改變形狀。"),
             ("長方形和正方形有什麼一樣？", "都有 4 條邊、4 個角", ["4 條邊都一樣長", "都沒有角", "都有 3 條邊"], "兩個都有 4 條邊、4 個直角，正方形的 4 條邊還一樣長。"),
             ("2 個一樣的三角形可以拼成什麼？", "正方形或長方形", ["圓形", "球", "圓柱"], "兩個一樣的直角三角形可以拼成正方形或長方形。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])
    return out + pick_unique(R, mk, 14, seen)


def s4(seen):
    def name():
        k = R.choice(list(SO))
        c = R.choice(["yellow", "red", "blue", "green"])
        q = "這個立體是什麼？" + P.solids_row([(k, c)])
        return mcq(q, SO[k], [v for x, v in SO.items() if x != k], {"sphere": "圓圓的，每一面都會滾，是球。", "cube": "6 個面都是一樣大的正方形，是正方體。", "cylinder": "上下是兩個圓，可以立著也可以滾，是圓柱。", "cone": "下面是圓，上面尖尖的，是圓錐。"}[k])
    FACTS = [("哪一個放在斜坡上，怎麼放都會滾？", "球", ["正方體", "圓柱", "圓錐"], "球每一面都是圓的，怎麼放都會滾。"),
             ("哪一個很容易一個一個疊高？", "正方體", ["球", "圓錐", "圓柱倒著放"], "正方體的面平平的，容易疊高。"),
             ("圓柱怎麼放才會滾？", "躺著放", ["立著放", "倒過來立著放", "不會滾"], "圓柱躺著放時，彎彎的面在下面，會滾。"),
             ("圓錐的頂端是什麼樣子？", "尖尖的", ["平平的", "圓圓的面", "有正方形的面"], "圓錐上面尖尖的，下面是圓形。"),
             ("正方體的每一個面是什麼形狀？", "正方形", ["圓形", "三角形", "長方形"], "正方體 6 個面都是一樣大的正方形。"),
             ("把圓柱立著蓋印，會印出什麼形狀？", "圓形", ["正方形", "三角形", "長方形"], "圓柱上下的面是圓形。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])
    return out + pick_unique(R, name, 14, seen)


def s5(seen):
    OBJ = [("籃球", "球", "立體"), ("骰子", "正方體", "立體"), ("鉛筆盒的蓋子", "長方形", "平面"), ("時鐘的鐘面", "圓形", "平面"),
           ("飲料罐", "圓柱", "立體"), ("冰淇淋甜筒", "圓錐", "立體"), ("三角板", "三角形", "平面"), ("方形餅乾", "正方形", "平面"),
           ("硬幣的一面", "圓形", "平面"), ("黑板", "長方形", "平面"), ("彈珠", "球", "立體"), ("衛生紙捲", "圓柱", "立體"),
           ("魔術方塊", "正方體", "立體"), ("三角飯糰的一面", "三角形", "平面"), ("聖誕帽", "圓錐", "立體"), ("門", "長方形", "平面"),
           ("西瓜", "球", "立體"), ("車子的輪子（正面看）", "圓形", "平面"), ("便利貼", "正方形", "平面"), ("交通錐（三角錐）", "圓錐", "立體")]
    out = []
    for o, shp, kind in OBJ:
        pool = list(SH.values()) if kind == "平面" else list(SO.values())
        w = [x for x in pool if x != shp]
        out.append(mcq("「%s」最像哪一種形狀？" % o, shp, w, "%s像%s。" % (o, shp)))
    return out


def main():
    seen = set()
    sets = [("認識平面圖形", s1(seen)), ("數一數形狀", s2(seen)), ("邊和角", s3(seen)),
            ("認識立體", s4(seen)), ("生活中的形狀", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["平面圖形：" + P.shapes_row([("triangle", "red"), ("square", "blue"), ("rectangle", "yellow"), ("circle", "green")], ["三角形", "正方形", "長方形", "圓形"]),
         "三角形有 <b>3 條邊、3 個角</b>；正方形、長方形有 <b>4 條邊、4 個角</b>；圓形沒有邊和角。",
         "立體：" + P.solids_row([("sphere", "red"), ("cube", "yellow"), ("cylinder", "blue"), ("cone", "green")], ["球", "正方體", "圓柱", "圓錐"]),
         "球怎麼放都會滾；正方體容易疊高；圓柱躺著會滾、立著可以疊。"],
        [example("正方形有幾個角？", ["數一數四個角落。"], "4 個"),
         example("飲料罐像哪一種立體？", ["上下是圓，身體彎彎的。"], "圓柱")],
        [("正方形轉個方向就不是正方形", "轉方向形狀不會變"),
         ("長方形和正方形一樣", "正方形 4 條邊一樣長"),
         ("圓形有 1 個角", "圓形沒有角")])
    faq = [{"q": "一年級要認識哪些形狀？",
            "a": "108課綱 S-1-1、S-1-2：以操作為主，認識三角形、正方形、長方形、圓形，和球、正方體、圓柱、圓錐等立體，會分類、堆疊、組合。"},
           {"q": "怎麼讓孩子分清正方形和長方形？",
            "a": "用尺或紙條量一量四條邊：四條都一樣長是正方形，長的和短的不一樣是長方形。"},
           {"q": "在家可以怎麼玩？",
            "a": "找家裡的東西說說像什麼形狀，例如時鐘像圓形、骰子像正方體，或用積木疊疊看哪些容易疊、哪些會滾。"}]
    make_unit(R, "grade-1", "shapes", "S-1-1",
              "形體的操作：以操作活動為主。描繪、分類、堆疊、組合。",
              "認識形狀：平面圖形和立體",
              "一年級數學 認識形狀 練習題｜三角形・正方形・圓形・正方體・圓柱 學習單（附解答）",
              "認識形狀",
              "國小一年級數學「認識形狀」免費學習單：認識三角形、正方形、長方形、圓形，數一數形狀、邊和角，認識球、正方體、圓柱、圓錐，生活中的形狀。100題線上練習，圖多，附可列印解答。",
              "三角形 3 個角，正方形、長方形 4 個角",
              "圓形沒有角；球怎麼放都會滾。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
