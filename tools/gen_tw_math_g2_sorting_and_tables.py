# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：分類與整理（108課綱 D-2-1）
  python3 tools/gen_tw_math_g2_sorting_and_tables.py
形・色で分類して數える、分類の中でさらに分類（紅色的三角形）、分類の規則を見つける、二つの觀點の表（色 × 形）を讀む、表から合計・差。
誤答：二つの條件の片方だけで數える、表の行と列の取り違え、合計で一つ數え落とす。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, table
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81318)
SHN = {"triangle": "三角形", "square": "正方形", "circle": "圓形"}
CN = {"red": "紅色", "blue": "藍色", "yellow": "黃色"}


def items(n):
    return [(R.choice(list(SHN)), R.choice(list(CN))) for _ in range(n)]


def s1(seen):
    def mk():
        its = items(R.randint(6, 7))
        by = R.choice(["color", "shape"])
        if by == "color":
            c = R.choice(list(CN))
            v = sum(1 for _, x in its if x == c)
            q = "%s的圖形有幾個？" % CN[c]
        else:
            c = R.choice(list(SHN))
            v = sum(1 for x, _ in its if x == c)
            q = "%s有幾個？" % SHN[c]
        if v == 0:
            return None
        q += P.shapes_row(its, size=20)
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (v + 1, v + 2, len(its), v - 1 if v > 1 else 0) if x != v][:3], "按%s分，%s有 %d 個。" % ("顏色" if by == "color" else "形狀", CN.get(c, SHN.get(c)), v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        its = items(7)
        s_, c = R.choice(list(SHN)), R.choice(list(CN))
        v = sum(1 for a, b in its if a == s_ and b == c)
        only_s = sum(1 for a, _ in its if a == s_)
        only_c = sum(1 for _, b in its if b == c)
        if v == 0 or only_s == v or only_c == v:
            return None
        q = "%s的%s有幾個？" % (CN[c], SHN[s_]) + P.shapes_row(its, size=20)
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (only_s, only_c, v + 1)], "先找%s，再從裡面找%s的：%d 個。" % (SHN[s_], CN[c], v))
    return pick_unique(R, mk, 20, seen)


GROUPS = [("會飛的", ["麻雀", "老鷹", "蝴蝶", "蜜蜂"], "不會飛的", ["小狗", "小貓", "兔子", "烏龜"], "會不會飛"),
          ("水果", ["蘋果", "香蕉", "葡萄", "芒果"], "蔬菜", ["高麗菜", "紅蘿蔔", "青椒", "菠菜"], "是水果還是蔬菜"),
          ("會滾的", ["球", "圓柱罐頭", "彈珠", "籃球"], "不會滾的", ["骰子", "面紙盒", "積木", "書本"], "會不會滾"),
          ("比 10 大的數", ["12", "15", "18", "20"], "比 10 小的數", ["2", "5", "7", "9"], "比 10 大還是小"),
          ("有 4 條邊的", ["正方形", "長方形", "窗戶", "書本封面"], "有 3 條邊的", ["三角形", "三角板", "三角形路標", "三角形旗子"], "邊的數量"),
          ("在水裡生活的", ["魚", "章魚", "海豚", "螃蟹"], "在陸地生活的", ["大象", "長頸鹿", "獅子", "老虎"], "生活在哪裡"),
          ("文具", ["鉛筆", "尺", "橡皮擦", "剪刀"], "餐具", ["湯匙", "筷子", "碗", "盤子"], "是文具還是餐具"),
          ("交通工具", ["公車", "火車", "腳踏車", "飛機"], "家具", ["桌子", "椅子", "床", "衣櫃"], "是交通工具還是家具")]


def s3(seen):
    out = []
    for a, xs, b, ys, rule in GROUPS:
        others = [g[4] for g in GROUPS if g[4] != rule]
        R.shuffle(others)
        out.append(mcq("甲組：%s；乙組：%s。是用什麼分類的？" % ("、".join(xs), "、".join(ys)), rule, others[:3], "甲組都是%s，乙組都是%s，按「%s」分類。" % (a, b, rule)))
        item = R.choice(xs)
        out.append(mcq("按「%s」分類，「%s」要放在哪一組？（甲組：%s的；乙組：%s的）" % (rule, item, a.rstrip("的"), b.rstrip("的")), "甲組", ["乙組", "兩組都可以", "都不行"], "%s是%s，放甲組。" % (item, a)))
    out += [mcq("同一堆東西，可以用不同的方法分類嗎？", "可以，例如按顏色或按形狀", ["不可以，只有一種分法", "只能按大小分", "只能按顏色分"], "分類的方法不只一種，只要說得出規則就可以。"),
            mcq("紅色的積木裡，再分成「大的」和「小的」，這叫什麼？", "分類中再分類", ["不能這樣分", "重新數一數", "合起來"], "分好的一類裡面，還可以用另一個方法再分。"),
            mcq("把 20 張卡片按顏色分成 3 堆，3 堆合起來一共有幾張？", "20 張", ["3 張", "23 張", "17 張"], "分類不會改變總數，合起來還是 20 張。"),
            mcq("分類時，一個東西可以同時放進兩組嗎？", "不行，每個東西只放一組", ["可以，隨便放", "一定要放兩組", "看心情"], "按一個規則分類，每個東西只會屬於一組。")]
    for b in out:
        seen.add(b["q"])
    return out[:20]


def tbl():
    nums = [[R.randint(1, 8) for _ in range(3)] for _ in range(2)]
    t = table(["", "三角形", "正方形", "圓形"], [["紅色"] + [str(x) for x in nums[0]], ["藍色"] + [str(x) for x in nums[1]]])
    return nums, t


def s4(seen):
    def mk():
        nums, t = tbl()
        k = R.choice(["cell", "shape", "color"])
        sh = ["三角形", "正方形", "圓形"]
        co = ["紅色", "藍色"]
        if k == "cell":
            i, j = R.randrange(2), R.randrange(3)
            v = nums[i][j]
            q = "下表是積木的分類。%s的%s有幾個？" % (co[i], sh[j]) + t
            w = [nums[1 - i][j], nums[i][(j + 1) % 3], v + 1]
            e = "找%s那一列、%s那一行：%d 個。" % (co[i], sh[j], v)
        elif k == "shape":
            j = R.randrange(3)
            v = nums[0][j] + nums[1][j]
            q = "下表是積木的分類。%s一共有幾個？" % sh[j] + t
            w = [nums[0][j], nums[1][j], v + 1]
            e = "紅色 %d 個 ＋ 藍色 %d 個 ＝ %d 個。" % (nums[0][j], nums[1][j], v)
        else:
            i = R.randrange(2)
            v = sum(nums[i])
            q = "下表是積木的分類。%s的積木一共有幾個？" % co[i] + t
            w = [sum(nums[1 - i]), nums[i][0], v + 1]
            e = "%s ＝ %d 個。" % (" ＋ ".join(map(str, nums[i])), v)
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in w if x != v] + ["%d 個" % (v + 2)], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        nums, t = tbl()
        k = R.choice(["total", "diff", "most"])
        sh = ["三角形", "正方形", "圓形"]
        if k == "total":
            v = sum(nums[0]) + sum(nums[1])
            q = "下表是積木的分類。積木一共有幾個？" + t
            return mcq(q, "%d 個" % v, ["%d 個" % x for x in (sum(nums[0]), v - 1, v + 1)], "全部加起來：%d 個。" % v)
        if k == "diff":
            j = R.randrange(3)
            if nums[0][j] == nums[1][j]:
                return None
            d = abs(nums[0][j] - nums[1][j])
            more = "紅色" if nums[0][j] > nums[1][j] else "藍色"
            less = "藍色" if more == "紅色" else "紅色"
            q = "下表是積木的分類。%s的%s比%s的多幾個？" % (more, sh[j], less) + t
            return mcq(q, "%d 個" % d, ["%d 個" % x for x in (nums[0][j] + nums[1][j], max(nums[0][j], nums[1][j]), d + 1)], "%d － %d ＝ %d。" % (max(nums[0][j], nums[1][j]), min(nums[0][j], nums[1][j]), d))
        tot = [nums[0][j] + nums[1][j] for j in range(3)]
        if len(set(tot)) < 3:
            return None
        j = tot.index(max(tot))
        q = "下表是積木的分類。哪一種形狀的積木最多？" + t
        return mcq(q, sh[j], [x for x in sh if x != sh[j]] + ["一樣多"], "每種形狀加起來：%s，%s最多。" % ("、".join("%s %d" % (sh[k2], tot[k2]) for k2 in range(3)), sh[j]))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("按顏色、形狀分", s1(seen)), ("分類中再分類", s2(seen)), ("分類的規則", s3(seen)),
            ("看分類表", s4(seen)), ("用表回答問題", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>分類</b>可以按顏色、形狀、大小……分，每個東西只放進一組。",
         "<b>分類中再分類</b>：先分出三角形，再從三角形裡分出紅色的。",
         "用<b>表</b>記錄兩種分法，一眼就看出「紅色的三角形」有幾個。" + table(["", "三角形", "正方形", "圓形"], [["紅色", "3", "2", "4"], ["藍色", "1", "5", "2"]])],
        [example("上表，紅色的圓形有幾個？", ["紅色那一列、圓形那一行。"], "4 個"),
         example("上表，正方形一共有幾個？", ["2 ＋ 5。"], "7 個")],
        [("紅色的三角形，數成所有紅色的", "兩個條件都要符合"),
         ("表看錯列和行", "先找列（顏色），再找行（形狀）"),
         ("一個東西放兩組", "按一個規則分，只放一組")])
    faq = [{"q": "二年級的統計要學什麼？",
            "a": "108課綱 D-2-1：蒐集、分類、記錄和呈現資料，並討論分類之中還可以再分類的情況。"},
           {"q": "為什麼要用表？",
            "a": "同時用兩種方法分類時，表可以把每一種的數量整理清楚，比一個一個找快。"},
           {"q": "在家怎麼練？",
            "a": "整理玩具時，先按種類分，再在每一類裡按顏色分，最後畫一個簡單的表。"}]
    make_unit(R, "grade-2", "sorting-and-tables", "D-2-1",
              "分類與呈現：以操作活動為主。能蒐集、分類、記錄、呈現資料、生活物件或幾何形體。討論分類之中還可以再分類的情況。",
              "分類與整理：用表記錄",
              "二年級數學 分類與整理 練習題｜分類中再分類・看分類表 學習單（附解答）",
              "分類與整理",
              "國小二年級數學「分類與整理」免費學習單：按顏色和形狀分類、分類中再分類、找分類的規則、看顏色和形狀的分類表、用表回答問題。100題線上練習，附可列印解答。",
              "分類中還可以再分類",
              "用表記錄兩種分法，先找列再找行。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
