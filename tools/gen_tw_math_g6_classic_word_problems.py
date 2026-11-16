# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：和差、雞兔、年齡、流水問題（108課綱 R-6-4、N-6-9）
  python3 tools/gen_tw_math_g6_classic_word_problems.py
和差問題（(和＋差)÷2）、雞兔問題（全部雞と假設して足の差で調整）、年齡問題（年齡差は不變）、流水問題（順水＝船速＋水速、逆水＝船速－水速）、綜合。
誤答：和差で (和−差)÷2 を大きい方とする、雞兔で假設した方を答える、年齡差が増えると思う、流水で水速を足し引き逆にする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names

R = random.Random(61016)
NM = Names(R)


def s1(seen):
    def mk():
        big, small = R.randint(20, 90), R.randint(5, 60)
        if big <= small:
            return None
        s, d = big + small, big - small
        n1, n2 = NM.next(), NM.next()
        if n1 == n2:
            return None
        ask = R.choice(["big", "small"])
        q = "%s和%s一共有 %d 張卡片，%s比%s多 %d 張。%s有幾張？" % (n1, n2, s, n1, n2, d, n1 if ask == "big" else n2)
        v = big if ask == "big" else small
        o = small if ask == "big" else big
        return mcq(q, "%d 張" % v, ["%d 張" % x for x in (o, s // 2 if s // 2 != v else v + 1, s - d)  if x != v] + ["%d 張" % (v + d)],
                   "大的 ＝（和 ＋ 差）÷ 2 ＝（%d ＋ %d）÷ 2 ＝ %d；小的 ＝（和 － 差）÷ 2 ＝ %d。" % (s, d, big, small))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        heads = R.randint(8, 40)
        rab = R.randint(1, heads - 1)
        ch = heads - rab
        legs = ch * 2 + rab * 4
        ask = R.choice(["rab", "ch"])
        q = "籠子裡有雞和兔子共 %d 隻，腳共 %d 隻。%s有幾隻？" % (heads, legs, "兔子" if ask == "rab" else "雞")
        v = rab if ask == "rab" else ch
        o = ch if ask == "rab" else rab
        return mcq(q, "%d 隻" % v, ["%d 隻" % x for x in (o, legs // 4 if legs // 4 not in (v, o) else v + 2, (legs - heads * 2))  if x != v and x > 0] + ["%d 隻" % (v + 1)],
                   "假設全是雞：%d × 2 ＝ %d 隻腳，少了 %d － %d ＝ %d 隻腳；每隻兔子比雞多 2 隻腳，兔子 ＝ %d ÷ 2 ＝ %d 隻，雞 ＝ %d 隻。" % (heads, heads * 2, legs, heads * 2, legs - heads * 2, legs - heads * 2, rab, ch))

    def money():
        n = R.randint(8, 30)
        a = R.randint(1, n - 1)
        b = n - a
        tot = a * 10 + b * 5
        q = "小豬撲滿裡有 10 元和 5 元硬幣共 %d 枚，合計 %d 元。10 元硬幣有幾枚？" % (n, tot)
        return mcq(q, "%d 枚" % a, ["%d 枚" % x for x in (b, tot // 10, a + 1)  if x != a], "假設全是 5 元：%d × 5 ＝ %d 元，少了 %d 元；每枚 10 元多 5 元：%d ÷ 5 ＝ %d 枚。" % (n, n * 5, tot - n * 5, tot - n * 5, a))
    return pick_unique(R, mk, 13, seen) + pick_unique(R, money, 7, seen)


def s3(seen):
    def diff():
        kid = R.randint(6, 13)
        gap = R.randint(24, 36)
        k = R.randint(3, 15)
        who = NM.next()
        q = "今年%s %d 歲，媽媽 %d 歲。%d 年後，媽媽比%s大幾歲？" % (who, kid, kid + gap, k, who)
        return mcq(q, "%d 歲" % gap, ["%d 歲" % x for x in (gap + k, gap - k, gap + 2 * k)], "兩人每年都長 1 歲，年齡差永遠不變：%d － %d ＝ %d。" % (kid + gap, kid, gap))

    def times():
        kid = R.randint(4, 12)
        m = R.choice([3, 4, 5])
        mom = kid * m
        if mom < 25 or mom > 50:
            return None
        gap = mom - kid
        # 幾年後媽媽是孩子的 2 倍
        if gap % (2 - 1):
            return None
        later = gap - kid
        if later <= 0:
            return None
        who = NM.next()
        q = "今年媽媽 %d 歲，%s %d 歲。幾年後媽媽的年齡是%s的 2 倍？" % (mom, who, kid, who)
        return mcq(q, "%d 年後" % later, ["%d 年後" % x for x in (gap, later + 2, mom // 2 - kid if mom // 2 - kid not in (later, gap) else later + 4)  if x > 0], "年齡差 %d 歲不變；媽媽是 2 倍時，孩子剛好 %d 歲，%d － %d ＝ %d（年後）。" % (gap, gap, gap, kid, later))

    def sum_age():
        a, b = R.randint(8, 14), R.randint(35, 45)
        k = R.randint(3, 10)
        q = "今年爸爸和兒子的年齡和是 %d 歲。%d 年後，兩人的年齡和是幾歲？" % (a + b, k)
        return mcq(q, "%d 歲" % (a + b + 2 * k), ["%d 歲" % x for x in (a + b + k, a + b, a + b + 4 * k)], "兩人各長 %d 歲，和多 %d × 2 ＝ %d：%d ＋ %d ＝ %d（歲）。" % (k, k, 2 * k, a + b, 2 * k, a + b + 2 * k))
    return pick_unique(R, diff, 7, seen) + pick_unique(R, times, 6, seen) + pick_unique(R, sum_age, 7, seen)


def s4(seen):
    def speed():
        boat, water = R.randint(10, 30), R.randint(2, 6)
        kind = R.choice(["down", "up"])
        v = boat + water if kind == "down" else boat - water
        q = "一艘船在靜水中時速 %d 公里，河水的流速是時速 %d 公里。船%s時，時速是多少公里？" % (boat, water, "順水而下" if kind == "down" else "逆水而上")
        return mcq(q, "%d 公里" % v, ["%d 公里" % x for x in (boat - water if kind == "down" else boat + water, boat, water * 2 + boat)  if x != v], ("順水：船速 ＋ 水速 ＝ %d ＋ %d ＝ %d。" if kind == "down" else "逆水：船速 － 水速 ＝ %d － %d ＝ %d。") % (boat, water, v))

    def back():
        boat, water = R.randint(10, 30), R.randint(2, 8)
        down, up = boat + water, boat - water
        ask = R.choice(["boat", "water"])
        q = "一艘船順水時速 %d 公里，逆水時速 %d 公里。%s的時速是多少公里？" % (down, up, "船在靜水中" if ask == "boat" else "水流")
        v = boat if ask == "boat" else water
        return mcq(q, "%d 公里" % v, ["%d 公里" % x for x in (water if ask == "boat" else boat, down - up, (down + up))  if x != v], "船速 ＝（順水 ＋ 逆水）÷ 2 ＝ %d；水速 ＝（順水 － 逆水）÷ 2 ＝ %d。" % (boat, water))

    def time():
        boat, water = R.randint(12, 25), R.randint(2, 5)
        t = R.randint(2, 6)
        d = (boat + water) * t
        q = "一艘船靜水時速 %d 公里，水速每小時 %d 公里。順水航行 %d 公里，要幾小時？" % (boat, water, d)
        return mcq(q, "%d 小時" % t, ["%s 小時" % x for x in (d // boat if d % boat == 0 else t + 1, t + 2, d // (boat - water) if d % (boat - water) == 0 else t + 3)  if str(x) != str(t)], "順水時速 %d ＋ %d ＝ %d，%d ÷ %d ＝ %d（小時）。" % (boat, water, boat + water, d, boat + water, t))
    return pick_unique(R, speed, 7, seen) + pick_unique(R, back, 7, seen) + pick_unique(R, time, 6, seen)


def s5(seen):
    def which():
        F_ = [("知道兩數的和和差，求兩數，是什麼問題？", "和差問題", ["雞兔問題", "流水問題", "年齡問題"], "已知和與差：大數 ＝（和 ＋ 差）÷ 2。"),
              ("知道頭的總數和腳的總數，求雞和兔子各幾隻，是什麼問題？", "雞兔問題", ["和差問題", "流水問題", "年齡問題"], "用假設法：先假設全是雞。"),
              ("年齡問題中，哪一個數量永遠不變？", "兩人的年齡差", ["兩人的年齡和", "兩人的年齡比", "年齡的倍數"], "每過一年兩人都長 1 歲，差不變。"),
              ("順水時速 ＝ ？", "船速 ＋ 水速", ["船速 － 水速", "船速 × 水速", "（船速 ＋ 水速）÷ 2"], "水往下流會幫忙推船。"),
              ("逆水時速 ＝ ？", "船速 － 水速", ["船速 ＋ 水速", "水速 － 船速", "船速 ÷ 水速"], "逆流時水會把船往回推。"),
              ("雞兔問題假設全是雞，腳少了 20 隻，兔子有幾隻？", "10 隻", ["20 隻", "5 隻", "40 隻"], "每隻兔子比雞多 2 隻腳：20 ÷ 2 ＝ 10。")]
        return mcq(*R.choice(F_))

    def spider():
        n = R.randint(5, 20)
        a = R.randint(1, n - 1)
        b = n - a
        legs = a * 8 + b * 6
        q = "蜘蛛（8 隻腳）和蜻蜓（6 隻腳）共 %d 隻，腳共 %d 隻。蜘蛛有幾隻？" % (n, legs)
        return mcq(q, "%d 隻" % a, ["%d 隻" % x for x in (b, legs // 8, a + 2)  if x != a], "假設全是蜻蜓：%d × 6 ＝ %d，多出 %d 隻腳，每隻蜘蛛多 2 隻：%d ÷ 2 ＝ %d（隻）。" % (n, n * 6, legs - n * 6, legs - n * 6, a))

    def test():
        n = R.choice([20, 25])
        right = R.randint(12, n)
        wrong_ = n - right
        score = right * 5 - wrong_ * 2
        q = "考試共 %d 題，答對一題得 5 分，答錯一題扣 2 分（每題都有作答）。%s得了 %d 分，答對幾題？" % (n, NM.next(), score)
        return mcq(q, "%d 題" % right, ["%d 題" % x for x in (score // 5, wrong_, right - 1)  if x != right and x >= 0], "假設全對：%d × 5 ＝ %d 分，少了 %d 分；每錯一題少 5 ＋ 2 ＝ 7 分，錯 %d ÷ 7 ＝ %d 題，對 %d 題。" % (n, n * 5, n * 5 - score, n * 5 - score, wrong_, right))
    return pick_unique(R, which, 6, seen) + pick_unique(R, spider, 7, seen) + pick_unique(R, test, 7, seen)


def main():
    seen = set()
    sets = [("和差問題", s1(seen)), ("雞兔問題", s2(seen)), ("年齡問題", s3(seen)),
            ("流水問題", s4(seen)), ("綜合挑戰", s5(seen))]
    body = lesson(
        ["<b>和差問題</b>：大數 ＝（和 ＋ 差）÷ 2，小數 ＝（和 － 差）÷ 2。",
         "<b>雞兔問題</b>：先假設全是雞，算出少了幾隻腳，每隻兔子多 2 隻腳，就能求兔子。",
         "<b>年齡問題</b>：兩人的年齡差永遠不變。",
         "<b>流水問題</b>：順水 ＝ 船速 ＋ 水速，逆水 ＝ 船速 － 水速。"],
        [example("兩數和 50、差 12，大數是多少？", ["（50 ＋ 12）÷ 2 ＝ 31。"], "31"),
         example("雞兔共 10 隻，腳 28 隻，兔子幾隻？", ["全是雞：10 × 2 ＝ 20 隻腳。", "少 8 隻，8 ÷ 2 ＝ 4。"], "4 隻")],
        [("大數 ＝（和 － 差）÷ 2", "那是小數；大數要加差"),
         ("雞兔問題答成假設的那一種", "算出來的是沒有假設的那一種"),
         ("過了 5 年，年齡差也多 5", "兩人都長 5 歲，差不變")])
    faq = [{"q": "雞兔問題怎麼教孩子理解？",
            "a": "先請孩子想像所有動物都抬起兩隻腳，剩下的腳都是兔子的，每隻兔子剩 2 隻，再除以 2 就是兔子數。"},
           {"q": "為什麼年齡差不會變？",
            "a": "每過一年，兩個人都長 1 歲，所以相差的歲數一直一樣。"},
           {"q": "六年級為什麼要學這些問題？",
            "a": "108課綱 R-6-4、N-6-9：由問題中的數量關係列出恰當的算式解題，包含年齡問題、流水問題、和差問題、雞兔問題等較複雜的情境。"}]
    make_unit(R, "grade-6", "classic-word-problems", "R-6-4",
              "解題：由問題中的數量關係，列出恰當的算式解題（同 N-6-9）。可包含（1）較複雜的模式（如座位排列模式）；（2）較複雜的計數：乘法原理、加法原理或其混合；（3）較複雜之情境：如年齡問題、流水問題、和差問題、雞兔問題。",
              "和差、雞兔、年齡、流水問題",
              "六年級數學 雞兔同籠 練習題｜和差問題・年齡問題・流水問題 學習單（附解答）",
              "和差、雞兔、年齡、流水",
              "國小六年級數學「和差、雞兔、年齡、流水問題」免費學習單：和差問題、雞兔同籠的假設法、年齡差不變、順水和逆水的速度與綜合挑戰題。100題線上練習馬上對答案，附可列印解答。",
              "雞兔問題：先假設全是雞",
              "和差：大數 ＝（和 ＋ 差）÷ 2；年齡差永遠不變。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
