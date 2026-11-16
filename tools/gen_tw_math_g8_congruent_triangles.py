# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：三角形的全等性質（108課綱 S-8-4、S-8-5）
  python3 tools/gen_tw_math_g8_congruent_triangles.py
全等の記號と對應（頂點の順序）、對應邊・對應角の長さと角度、SSS・SAS・ASA・AAS・RHS の判定、SSA・AAA は不一定、幾何の場面、式で表した邊。
誤答：頂點の順序を無視して對應をとる、夾角でない角で SAS とする、AAA を全等とする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets

R = random.Random(81020)
PAIRS = [("ABC", "DEF"), ("ABC", "PQR"), ("PQR", "XYZ"), ("ABC", "LMN"), ("DEF", "STU"), ("KLM", "XYZ")]


def tri():
    a, b = R.choice(PAIRS)
    perm = list(range(3))
    R.shuffle(perm)
    b = "".join(b[i] for i in perm)
    return a, b


def side(t, i, j):
    return "<span class='ov'>%s%s</span>" % (t[i], t[j])


def s1(seen):
    def corr_side():
        a, b = tri()
        i, j = R.sample(range(3), 2)
        q = "△%s ≅ △%s，%s 的對應邊是哪一邊？" % (a, b, side(a, i, j))
        ans = side(b, i, j)
        others = [side(b, x, y) for x, y in ((0, 1), (1, 2), (0, 2)) if {x, y} != {i, j}] + [side(a, i, j)]
        return mcq(q, ans, others, "全等記號的頂點按順序對應：%s↔%s、%s↔%s、%s↔%s，所以 %s 對應 %s。" % (a[0], b[0], a[1], b[1], a[2], b[2], side(a, i, j), ans))

    def corr_ang():
        a, b = tri()
        i = R.randrange(3)
        q = "△%s ≅ △%s，∠%s 的對應角是哪一個角？" % (a, b, a[i])
        return mcq(q, "∠%s" % b[i], ["∠%s" % b[k] for k in range(3) if k != i] + ["∠%s" % a[(i + 1) % 3]], "按頂點順序：第 %d 個字母 %s 對應 %s，所以是 ∠%s。" % (i + 1, a[i], b[i], b[i]))
    return pick_unique(R, corr_side, 10, seen) + pick_unique(R, corr_ang, 10, seen)


def s2(seen):
    def sidelen():
        a, b = tri()
        L = [R.randint(4, 15) for _ in range(3)]
        if len(set(L)) < 3 or max(L) * 2 >= sum(L):
            return None
        i, j = 0, 1
        k = R.choice([(0, 1), (1, 2), (0, 2)])
        given = "、".join("%s ＝ %d" % (side(a, x, y), L[n]) for n, (x, y) in enumerate(((0, 1), (1, 2), (0, 2))))
        idx = [(0, 1), (1, 2), (0, 2)].index(k)
        q = "△%s ≅ △%s，%s，%s 是多少？" % (a, b, given, side(b, *k))
        return mcq(q, str(L[idx]), [str(L[(idx + 1) % 3]), str(L[(idx + 2) % 3]), str(sum(L))], "%s 對應 %s，對應邊相等：%d。" % (side(b, *k), side(a, *k), L[idx]))

    def angle():
        a, b = tri()
        x, y = R.randint(30, 80), R.randint(30, 80)
        z = 180 - x - y
        if z < 20 or len({x, y, z}) < 3:
            return None
        q = "△%s ≅ △%s，∠%s ＝ %d°，∠%s ＝ %d°，∠%s 是多少度？" % (a, b, a[0], x, a[1], y, b[2])
        return mcq(q, "%d°" % z, ["%d°" % v for v in (x, y, 180 - z, 90 - z if 90 - z > 0 else z + 10)], "∠%s ＝ 180° － %d° － %d° ＝ %d°，∠%s 對應 ∠%s，所以是 %d°。" % (a[2], x, y, z, b[2], a[2], z))
    return pick_unique(R, sidelen, 10, seen) + pick_unique(R, angle, 10, seen)


PROPS = ["SSS", "SAS", "ASA", "AAS", "RHS", "不一定全等"]


def s3(seen):
    def mk():
        a, b = "ABC", "DEF"
        t = R.choice(["SSS", "SAS", "ASA", "AAS", "RHS", "SSA", "AAA"])
        S = lambda i, j: "%s ＝ %s" % (side(a, i, j), side(b, i, j))
        A = lambda i: "∠%s ＝ ∠%s" % (a[i], b[i])
        if t == "SSS":
            c = [S(0, 1), S(1, 2), S(0, 2)]
        elif t == "SAS":
            v = R.randrange(3)
            o = [k for k in range(3) if k != v]
            c = [S(v, o[0]), A(v), S(v, o[1])]
        elif t == "ASA":
            i, j = R.sample(range(3), 2)
            c = [A(i), S(i, j), A(j)]
        elif t == "AAS":
            i, j = R.sample(range(3), 2)
            k = 3 - i - j
            c = [A(i), A(j), S(j, k)]
        elif t == "RHS":
            v = R.randrange(3)
            o = [k for k in range(3) if k != v]
            c = ["∠%s ＝ ∠%s ＝ 90°" % (a[v], b[v]), S(o[0], o[1]), S(v, o[0])]
        elif t == "SSA":
            v = R.randrange(3)
            o = [k for k in range(3) if k != v]
            c = [S(v, o[0]), S(o[0], o[1]), A(o[1])]
        else:
            c = [A(0), A(1), A(2)]
        R.shuffle(c)
        ans = t if t in PROPS else "不一定全等"
        q = "△ABC 和 △DEF 中，%s。兩個三角形依據哪一個性質全等？" % "，".join(c)
        why = {"SSS": "三邊對應相等。", "SAS": "兩邊和它們的夾角對應相等。", "ASA": "兩角和它們的夾邊對應相等。", "AAS": "兩角和其中一角的對邊對應相等。",
               "RHS": "直角三角形的斜邊和一股對應相等。", "不一定全等": "兩邊和非夾角（SSA）或三個角（AAA）相等，都不能確定全等。"}[ans]
        return mcq(q, ans, [p for p in PROPS if p != ans], why)
    return pick_unique(R, mk, 20, seen)


SCENES = [
    ("四邊形 ABCD 中，<span class='ov'>AB</span> ＝ <span class='ov'>AD</span>，<span class='ov'>CB</span> ＝ <span class='ov'>CD</span>，連對角線 <span class='ov'>AC</span>。△ABC 和 △ADC 依據哪一個性質全等？", "SSS", "AC 是共用邊，加上兩組邊相等，三邊相等。"),
    ("<span class='ov'>AB</span> 和 <span class='ov'>CD</span> 交於 O，O 是兩線段的中點。△AOC 和 △BOD 依據哪一個性質全等？", "SAS", "OA ＝ OB、OC ＝ OD，夾角 ∠AOC 和 ∠BOD 是對頂角相等。"),
    ("等腰三角形 ABC 中，<span class='ov'>AB</span> ＝ <span class='ov'>AC</span>，<span class='ov'>AD</span> 是頂角 ∠A 的角平分線。△ABD 和 △ACD 依據哪一個性質全等？", "SAS", "AB ＝ AC，∠BAD ＝ ∠CAD，AD 是共用邊。"),
    ("等腰三角形 ABC 中，<span class='ov'>AB</span> ＝ <span class='ov'>AC</span>，<span class='ov'>AD</span> ⊥ <span class='ov'>BC</span> 於 D。△ABD 和 △ACD 依據哪一個性質全等？", "RHS", "兩個都是直角三角形，斜邊 AB ＝ AC，股 AD 共用。"),
    ("∠ABC 的角平分線上一點 P，從 P 畫 <span class='ov'>PD</span> ⊥ <span class='ov'>BA</span>、<span class='ov'>PE</span> ⊥ <span class='ov'>BC</span>。△PBD 和 △PBE 依據哪一個性質全等？", "AAS", "∠PBD ＝ ∠PBE，∠PDB ＝ ∠PEB ＝ 90°，PB 共用（是直角的對邊）。"),
    ("平行四邊形 ABCD 的對角線 <span class='ov'>AC</span>，△ABC 和 △CDA 依據哪一個性質全等？（利用 AB // CD、AD // BC）", "ASA", "內錯角 ∠BAC ＝ ∠DCA、∠BCA ＝ ∠DAC，夾邊 AC 共用。"),
    ("<span class='ov'>AB</span> ＝ <span class='ov'>DC</span>，<span class='ov'>AC</span> ＝ <span class='ov'>DB</span>，B、C 在同一條線上，△ABC 和 △DCB 依據哪一個性質全等？", "SSS", "AB ＝ DC、AC ＝ DB，BC 是共用邊。"),
    ("兩個三角形的三個角分別是 50°、60°、70°，它們一定全等嗎？", "不一定全等", "三個角相等只能說形狀一樣，大小可能不同（AAA 不是全等性質）。"),
]


def s4(seen):
    out = [mcq(q, a, [p for p in PROPS if p != a], e) for q, a, e in SCENES]
    for b in out:
        seen.add(b["q"])

    def which():
        t = R.choice(["SAS", "ASA", "SSS"])
        a, b = tri()
        if t == "SAS":
            ask = "∠%s ＝ ∠%s" % (a[1], b[1])
            known = "%s ＝ %s，%s ＝ %s" % (side(a, 0, 1), side(b, 0, 1), side(a, 1, 2), side(b, 1, 2))
            w = ["∠%s ＝ ∠%s" % (a[0], b[0]), "∠%s ＝ ∠%s" % (a[2], b[2]), "%s ＝ %s" % (side(a, 0, 1), side(b, 1, 2))]
        elif t == "ASA":
            ask = "%s ＝ %s" % (side(a, 0, 2), side(b, 0, 2))
            known = "∠%s ＝ ∠%s，∠%s ＝ ∠%s" % (a[0], b[0], a[2], b[2])
            w = ["%s ＝ %s" % (side(a, 0, 1), side(b, 0, 2)), "∠%s ＝ ∠%s" % (a[1], b[1]), "%s ＝ %s" % (side(a, 1, 2), side(b, 0, 1))]
        else:
            ask = "%s ＝ %s" % (side(a, 0, 2), side(b, 0, 2))
            known = "%s ＝ %s，%s ＝ %s" % (side(a, 0, 1), side(b, 0, 1), side(a, 1, 2), side(b, 1, 2))
            w = ["∠%s ＝ ∠%s" % (a[0], b[0]), "∠%s ＝ ∠%s" % (a[2], b[2]), "%s ＝ %s" % (side(a, 0, 2), side(b, 0, 1))]
        q = "要證明 △%s ≅ △%s（%s），已知 %s，還需要哪一個條件？" % (a, b, t, known)
        return mcq(q, ask, w, "%s：%s。" % (t, {"SAS": "需要兩邊的夾角", "ASA": "需要兩角的夾邊", "SSS": "需要第三組邊"}[t]))
    return out + pick_unique(R, which, 12, seen)


def s5(seen):
    def eq():
        a, b = tri()
        x = R.randint(2, 9)
        p, c = R.randint(2, 5), R.randint(-5, 8)
        v = p * x + c
        if v <= 0:
            return None
        q = "△%s ≅ △%s，%s ＝ %s，%s ＝ %d，x 是多少？" % (a, b, side(a, 0, 1), "%dx%s" % (p, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else ""), side(b, 0, 1), v)
        return mcq(q, str(x), [str(v), str(x + 1), str((v + c) // p) if (v + c) % p == 0 and (v + c) // p != x else str(x - 1)], "對應邊相等：%dx%s ＝ %d，x ＝ %d。" % (p, (" ＋ %d" % c) if c > 0 else (" － %d" % -c) if c else "", v, x))

    def perim():
        a, b = tri()
        L = sorted(R.sample(range(5, 20), 3))
        if L[0] + L[1] <= L[2]:
            return None
        q = "△%s ≅ △%s，△%s 的三邊長是 %d、%d、%d 公分，△%s 的周長是多少公分？" % (a, b, a, L[0], L[1], L[2], b)
        P = sum(L)
        return mcq(q, "%d 公分" % P, ["%d 公分" % v for v in (2 * P, L[2], L[0] * L[1] // 2, P - L[0])], "全等三角形的對應邊都相等，周長也相等：%d ＋ %d ＋ %d ＝ %d（公分）。" % (L[0], L[1], L[2], P))
    return pick_unique(R, eq, 12, seen) + pick_unique(R, perim, 8, seen)


def main():
    seen = set()
    sets = [("全等的對應", s1(seen)), ("對應邊和對應角", s2(seen)), ("判斷全等性質", s3(seen)),
            ("圖形中的全等", s4(seen)), ("用全等求值", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["兩個圖形能完全疊合叫<b>全等</b>，記成 △ABC ≅ △DEF，<b>頂點要按對應的順序寫</b>：A↔D、B↔E、C↔F。",
         "全等三角形的對應邊相等、對應角相等。",
         "判斷全等的五個性質：<b>SSS</b>（三邊）、<b>SAS</b>（兩邊夾一角）、<b>ASA</b>（兩角夾一邊）、<b>AAS</b>（兩角一對邊）、<b>RHS</b>（直角、斜邊、一股）。",
         "SSA（兩邊和非夾角）、AAA（三個角）<b>不一定全等</b>。"],
        [example("△ABC ≅ △PQR，∠A ＝ 40°，∠B ＝ 65°，∠R ＝ ？", ["R 對應 C。", "∠C ＝ 180° － 40° － 65° ＝ 75°。"], "75°"),
         example("AB ＝ DE，∠B ＝ ∠E，BC ＝ EF", ["∠B、∠E 是兩邊的夾角。"], "SAS")],
        [("△ABC ≅ △DEF，就說 AB 對應 EF", "按順序：AB 對應 DE"),
         ("兩邊和任意一角相等就是 SAS", "角一定要是兩邊的夾角"),
         ("三個角都相等就全等", "AAA 只保證形狀相同，大小可能不同")])
    faq = [{"q": "為什麼全等記號的字母順序很重要？",
            "a": "順序就代表對應關係，△ABC ≅ △DEF 表示 A 對 D、B 對 E、C 對 F，寫錯順序就會找錯對應邊和對應角。"},
           {"q": "RHS 和 SSA 有什麼不同？",
            "a": "RHS 只用在直角三角形，已知直角、斜邊和一股就能全等；一般三角形的 SSA 不一定全等。"},
           {"q": "八年級的全等要學什麼？",
            "a": "108課綱 S-8-4、S-8-5：全等圖形的意義和對應，三角形的全等性質 SSS、SAS、ASA、AAS、RHS。"}]
    make_unit(R, "grade-8", "congruent-triangles", "S-8-5",
              "三角形的全等性質：三角形的全等判定（SAS、SSS、ASA、AAS、RHS）；全等符號（≅）。",
              "三角形的全等性質",
              "八年級數學 全等三角形 練習題｜SSS・SAS・ASA・AAS・RHS 學習單（附解答）",
              "全等三角形",
              "國中八年級數學「三角形的全等性質」免費學習單：全等記號與對應頂點、對應邊和對應角、判斷 SSS、SAS、ASA、AAS、RHS、圖形中的全等、用全等求值。100題線上練習馬上對答案，附可列印解答。",
              "SSS、SAS、ASA、AAS、RHS",
              "頂點按順序對應；SSA、AAA 不一定全等。",
              body, faq, sets, 20)


if __name__ == "__main__":
    main()
