# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：球、柱體與錐體（108課綱 S-5-7）
  python3 tools/gen_tw_math_g5_solids.py
角柱・角錐の面・頂點・邊の数、底面と側面の形、柱体の 2 底面は平行・側面と底面は垂直、錐体は垂直でない、展開圖、生活の立體。
誤答：角錐の底面を 2 つとする、n 角柱の邊を n×2 とする、圓錐の側面を三角形とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names

R = random.Random(51023)
NM = Names(R)
POLY = {3: "三角", 4: "四角", 5: "五角", 6: "六角", 7: "七角", 8: "八角"}


def s1(seen):
    def mk():
        n = R.choice(list(POLY))
        kind = R.choice(["柱", "錐"])
        what = R.choice(["面", "頂點", "邊"])
        name = POLY[n] + kind
        if kind == "柱":
            v = {"面": n + 2, "頂點": 2 * n, "邊": 3 * n}[what]
            e = {"面": "上下 2 個底面 ＋ %d 個側面 ＝ %d" % (n, n + 2), "頂點": "上下各 %d 個 ＝ %d" % (n, 2 * n), "邊": "上下底各 %d 條 ＋ 側邊 %d 條 ＝ %d" % (n, n, 3 * n)}[what]
            w = {"面": [n + 1, 2 * n, n], "頂點": [n + 1, n, 3 * n], "邊": [2 * n, n + 2, 4 * n]}[what]
        else:
            v = {"面": n + 1, "頂點": n + 1, "邊": 2 * n}[what]
            e = {"面": "1 個底面 ＋ %d 個側面 ＝ %d" % (n, n + 1), "頂點": "底面 %d 個 ＋ 尖端 1 個 ＝ %d" % (n, n + 1), "邊": "底面 %d 條 ＋ 側邊 %d 條 ＝ %d" % (n, n, 2 * n)}[what]
            w = {"面": [n + 2, n, 2 * n], "頂點": [n, 2 * n, n + 2], "邊": [3 * n, n + 1, n]}[what]
        return mcq("%s有幾%s%s？" % (name, "條" if what == "邊" else "個", what), "%d 個" % v if what != "邊" else "%d 條" % v, [("%d 個" if what != "邊" else "%d 條") % x for x in w if x != v] + [("%d 個" if what != "邊" else "%d 條") % (v + 1)],
                   "%s：%s。" % (name, e))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.choice(list(POLY))
        kind = R.choice(["柱", "錐"])
        name = POLY[n] + kind
        ask = R.choice(["底", "側"])
        if ask == "底":
            ans = POLY[n] + "形" if n > 4 else ("三角形" if n == 3 else "四邊形（如長方形、正方形）")
            if n > 4:
                ans = POLY[n].replace("角", "邊") + "形"
            w = ["長方形" if kind == "錐" else "三角形", "圓形", POLY[n + 1 if n < 8 else 3].replace("角", "邊") + "形"]
            return mcq("（直）%s的底面是什麼形狀？" % name, ans, [x for x in w if x != ans] + ["五邊形" if ans != "五邊形" else "六邊形"], "%s的底面是%s。" % (name, ans))
        ans = "長方形" if kind == "柱" else "三角形"
        return mcq("（直）%s的側面是什麼形狀？" % name, ans, ["三角形" if ans == "長方形" else "長方形", "圓形", POLY[n].replace("角", "邊") + "形" if n != 4 else "梯形"], "直%s的側面都是%s。" % ("柱" if kind == "柱" else "錐", ans))

    def round_():
        F = [("圓柱的底面是什麼形狀？", "圓形", ["長方形", "三角形", "扇形"], "圓柱有上下兩個圓形底面。"),
             ("圓錐的底面是什麼形狀？", "圓形", ["三角形", "長方形", "扇形"], "圓錐有一個圓形底面。"),
             ("圓柱的側面攤開是什麼形狀？", "長方形", ["圓形", "扇形", "三角形"], "圓柱的側面沿直線剪開攤平是長方形。"),
             ("圓錐的側面攤開是什麼形狀？", "扇形", ["三角形", "長方形", "圓形"], "圓錐的側面攤開是扇形，不是三角形。"),
             ("球有幾個面？", "1 個曲面", ["沒有面", "2 個平面", "6 個面"], "球只有一個彎曲的面。"),
             ("哪一種立體沒有頂點也沒有邊？", "球", ["圓錐", "正方體", "三角柱"], "球只有一個曲面，沒有頂點和邊。")]
        return mcq(*R.choice(F))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, round_, 6, seen)


TRUE = ["柱體的兩個底面互相平行。", "直柱體的側面和底面互相垂直。", "錐體只有一個底面。", "直錐體的側面和底面不垂直。", "圓錐有一個頂點。", "長方體也是一種四角柱。"]
FALSE = ["錐體有兩個互相平行的底面。", "圓錐的側面攤開是三角形。", "三角錐有 6 個頂點。", "球有 2 個平面。", "五角柱有 5 個面。", "直柱體的側面和底面不垂直。"]


def s3(seen):
    def mk():
        ok = R.random() < .5
        ans = R.choice(TRUE if ok else FALSE)
        st = R.sample(FALSE if ok else TRUE, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        LET = "甲乙丙丁"
        q = "下面哪一句話是<b>%s</b>的？<br>%s" % ("對" if ok else "錯", "<br>".join("%s：%s" % (LET[i], t) for i, t in enumerate(st)))
        return mcq(q, LET[k], [l for l in LET if l != LET[k]], "%s是%s的。柱體有兩個平行的底面，側面和底面垂直；錐體只有一個底面，側面和底面不垂直。" % (LET[k], "對" if ok else "錯"))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def which():
        n = R.choice(list(POLY))
        kind = R.choice(["柱", "錐"])
        if kind == "柱":
            q = "一個立體的展開圖有 2 個%s形和 %d 個長方形，摺起來是什麼？" % (POLY[n].replace("角", "邊") if n > 3 else "三角", n)
            ans = POLY[n] + "柱"
            w = [POLY[n] + "錐", POLY[n + 1 if n < 8 else 3] + "柱", "圓柱"]
        else:
            q = "一個立體的展開圖有 1 個%s形和 %d 個三角形，摺起來是什麼？" % (POLY[n].replace("角", "邊") if n > 3 else "三角", n)
            ans = POLY[n] + "錐"
            w = [POLY[n] + "柱", POLY[n + 1 if n < 8 else 3] + "錐", "圓錐"]
        return mcq(q, ans, w, "%s：%s。" % (ans, "兩個平行的底面 ＋ 長方形側面" if kind == "柱" else "一個底面 ＋ 三角形側面"))

    def round_net():
        F = [("展開圖是 2 個圓和 1 個長方形，摺起來是什麼？", "圓柱", ["圓錐", "球", "四角柱"], "2 個圓是底面，長方形捲起來是側面。"),
             ("展開圖是 1 個圓和 1 個扇形，摺起來是什麼？", "圓錐", ["圓柱", "三角錐", "球"], "扇形捲起來是側面，圓是底面。")]
        return mcq(*R.choice(F))
    def parts():
        n = R.choice(list(POLY))
        kind = R.choice(["柱", "錐"])
        shape = "長方形" if kind == "柱" else "三角形"
        q = "%s%s的展開圖裡有幾個%s？" % (POLY[n], kind, shape)
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (n + 2 if kind == "柱" else n + 1, 2 * n, n - 1)],
                   "%s%s有 %d 個側面，每個側面都是%s。" % (POLY[n], kind, n, shape))
    return pick_unique(R, which, 10, seen) + pick_unique(R, parts, 8, seen) + pick_unique(R, round_net, 2, seen)


def s5(seen):
    LIFE = [("鉛筆盒（長方體）", "四角柱"), ("一罐汽水", "圓柱"), ("冰淇淋甜筒", "圓錐"), ("籃球", "球"), ("金字塔", "四角錐"),
            ("三角帳篷", "三角柱"), ("六角鉛筆", "六角柱"), ("生日帽", "圓錐"), ("骰子", "四角柱（正方體）")]
    out = []
    for it, ans in LIFE:
        opts = [x for x in ("四角柱", "圓柱", "圓錐", "球", "四角錐", "三角柱", "六角柱", "三角錐") if x != ans and not (ans.startswith("四角柱") and x == "四角柱")]
        R.shuffle(opts)
        out.append(mcq("%s最像哪一種立體？" % it, ans, opts[:3], "%s的形狀像%s。" % (it, ans)))
    for o in out:
        seen.add(o["q"])

    def count():
        n = R.choice(list(POLY))
        kind = R.choice(["柱", "錐"])
        k = 3 if kind == "柱" else 2
        tot = k * n
        nm = lambda x: {**POLY, 9: "九角", 10: "十角", 11: "十一角", 12: "十二角"}[x] + kind
        wrong = [tot // 2 if kind == "柱" and tot % 2 == 0 else tot // 3 if tot % 3 == 0 else n + 2, n + 1, n - 1, n + 2, n + 3]
        w = []
        for x in wrong:
            if x >= 3 and x != n and nm(x) not in w:
                w.append(nm(x))
        q = "一個角%s有 %d 條邊，它是幾角%s？" % (kind, tot, kind)
        return mcq(q, nm(n), w, "角%s的邊數是底面邊數的 %d 倍：%d ÷ %d ＝ %d，是%s。" % (kind, k, tot, k, n, nm(n)))
    return out + pick_unique(R, count, 20 - len(out), seen)


def main():
    seen = set()
    sets = [("面、頂點、邊的數量", s1(seen)), ("底面和側面", s2(seen)), ("柱體和錐體的性質", s3(seen)), ("展開圖", s4(seen)), ("生活中的立體", s5(seen))]
    body = lesson(
        ["<b>柱體</b>（角柱、圓柱）：有 2 個一樣大、<b>互相平行</b>的底面；直柱體的側面和底面<b>垂直</b>。",
         "<b>錐體</b>（角錐、圓錐）：只有 1 個底面和一個尖尖的頂點；側面和底面<b>不垂直</b>。",
         "n 角柱：面 n＋2、頂點 2n、邊 3n。n 角錐：面 n＋1、頂點 n＋1、邊 2n。",
         "圓柱的側面攤開是長方形，圓錐的側面攤開是扇形。球只有一個曲面。"],
        [example("五角柱有幾個面、幾個頂點、幾條邊？", ["面：5 ＋ 2 ＝ 7。", "頂點：5 × 2 ＝ 10；邊：5 × 3 ＝ 15。"], "7 個面、10 個頂點、15 條邊"),
         example("四角錐有幾條邊？", ["底面 4 條 ＋ 側邊 4 條。"], "8 條")],
        [("角錐有兩個底面", "錐體只有一個底面"),
         ("五角柱有 5 個面", "還有上下 2 個底面：7 個面"),
         ("圓錐的側面攤開是三角形", "是扇形")])
    faq = [{"q": "柱體和錐體有什麼不同？",
            "a": "柱體有兩個平行的底面，側面和底面垂直；錐體只有一個底面，往上收成一個頂點，側面和底面不垂直。"},
           {"q": "角柱和角錐的面、頂點、邊怎麼算？",
            "a": "n 角柱：面 n＋2、頂點 2n、邊 3n；n 角錐：面 n＋1、頂點 n＋1、邊 2n。"},
           {"q": "五年級的立體要學什麼？",
            "a": "108課綱 S-5-7：認識球、圓柱、角柱、角錐、圓錐，知道柱體和錐體的構成要素和展開圖，並檢查底面平行和側面垂直的性質。"}]
    make_unit(R, "grade-5", "solids", "S-5-7",
              "球、柱體與錐體：以操作活動為主。認識球、（直）圓柱、（直）角柱、（直）角錐、（直）圓錐。認識柱體和錐體之構成要素與展開圖。檢查柱體兩底面平行；檢查柱體側面和底面垂直，錐體側面和底面不垂直。",
              "球、柱體與錐體",
              "五年級數學 柱體錐體 練習題｜角柱・角錐・圓柱・圓錐 學習單（附解答）",
              "柱體與錐體",
              "國小五年級數學「球、柱體與錐體」免費學習單：角柱和角錐的面、頂點、邊的數量，底面和側面的形狀，柱體和錐體的性質、展開圖和生活中的立體。100題線上練習馬上對答案，附可列印解答。",
              "柱體兩個底面平行，錐體只有一個底面",
              "n 角柱：面 n＋2、頂點 2n、邊 3n。",
              body, faq, sets, 23)


if __name__ == "__main__":
    main()
