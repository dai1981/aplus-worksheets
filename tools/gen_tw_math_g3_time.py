# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：時間（日、時、分、秒）（108課綱 N-3-17）
  python3 tools/gen_tw_math_g3_time.py
時間單位的換算、時間量的加減、時刻＋時間量、兩個時刻之間經過多久、量感と應用問題。
時刻は「上午 9 時 40 分」、時間量は「1 小時 45 分鐘」（台灣の教科書の書き方）。
誤答：1 小時＝100 分鐘として計算、繰り上がり忘れ（1 小時 75 分鐘）、正午をまたぐ計算で 12 を忘れる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, clock

R = random.Random(31017)
NM = Names(R)


def tm(t):
    """t：0時からの分 → 上午 9 時 40 分"""
    h, m = divmod(t, 60)
    if h < 12:
        p, hh = "上午", h
    elif h == 12:
        p, hh = "中午", 12
    elif h < 18:
        p, hh = "下午", h - 12
    else:
        p, hh = "晚上", h - 12
    return "%s %d 時%s" % (p, hh, " %d 分" % m if m else "")


def hm(a, b):
    """誤答用：a 小時 b 分鐘（a が 0 なら分鐘だけ）"""
    return "%d 分鐘" % b if a == 0 else "%d 小時 %d 分鐘" % (a, b)


def du(m, unit=("小時", "分鐘")):
    a, b = divmod(m, 60)
    if a and b:
        return "%d %s %d %s" % (a, unit[0], b, unit[1])
    if a:
        return "%d %s" % (a, unit[0])
    return "%d %s" % (b, unit[1])


def ds(s):
    return du(s, ("分鐘", "秒"))


def s1(seen):
    def h2m():
        a, b = R.randint(1, 5), R.choice([0, 10, 15, 20, 25, 30, 40, 45, 50])
        v = a * 60 + b
        q = "%s ＝ ___ 分鐘" % du(v)
        return mcq(q, str(v), [str(x) for x in (a * 100 + b, a + b, a * 10 + b, v + 60)],
                   "1 小時 ＝ 60 分鐘，%s共 %d 分鐘。" % (("%d 小時 ＝ %d 分鐘，" % (a, a * 60) if a > 1 else "") + ("再加 %d，" % b if b else ""), v))

    def m2h():
        v = R.randint(65, 290)
        if v % 5:
            return None
        a, b = divmod(v, 60)
        if b == 0:
            return None
        q = "%d 分鐘 ＝ ___ 小時 ___ 分鐘" % v
        return mcq(q, du(v), ["%d 小時 %d 分鐘" % x for x in ((v // 100, v % 100) if v % 100 and v // 100 else (a + 1, b), (a - 1, b + 60) if a > 1 else (a, b + 10), (a + 1, b), (a, 60 - b) if 60 - b != b else (a, b + 5))],
                   "每 60 分鐘是 1 小時：%d ÷ 60 ＝ %d……%d，所以是 %s。" % (v, a, b, du(v)))

    def sec():
        if R.random() < .5:
            a, b = R.randint(1, 5), R.randint(5, 55)
            v = a * 60 + b
            q = "%s ＝ ___ 秒" % ds(v)
            return mcq(q, str(v), [str(x) for x in (a * 100 + b, a + b, v + 60, v - 60 if a > 1 else v + 120)], "1 分鐘 ＝ 60 秒，%s再加 %d 秒，共 %d 秒。" % ("%d 分鐘 ＝ %d 秒，" % (a, a * 60) if a > 1 else "", b, v))
        v = R.randint(65, 290)
        a, b = divmod(v, 60)
        if b == 0:
            return None
        return mcq("%d 秒 ＝ ___ 分鐘 ___ 秒" % v, ds(v), ["%d 分鐘 %d 秒" % x for x in ((a + 1, b), (a - 1, b + 60) if a > 1 else (a, b + 10), (v // 100 or a + 2, v % 100 or 1))],
                   "每 60 秒是 1 分鐘：%d 秒 ＝ %s。" % (v, ds(v)))

    def day():
        if R.random() < .5:
            d, h = R.randint(1, 4), R.randint(0, 20)
            v = d * 24 + h
            q = "%d 日%s ＝ ___ 小時" % (d, " %d 小時" % h if h else "")
            return mcq(q, str(v), [str(x) for x in (d * 12 + h, d * 60 + h, d * 10 + h, v + 24)], "1 日 ＝ 24 小時，%s共 %d 小時。" % (("%d 日 ＝ %d 小時，" % (d, d * 24) if d > 1 else "") + ("再加 %d，" % h if h else ""), v))
        v = R.randint(26, 100)
        d, h = divmod(v, 24)
        if h == 0:
            return None
        return mcq("%d 小時 ＝ ___ 日 ___ 小時" % v, "%d 日 %d 小時" % (d, h),
                   ["%d 日 %d 小時" % x for x in ((d + 1, h), (d - 1, h + 24) if d > 1 else (d, h + 12), (v // 12, v % 12) if v % 12 else (d, h + 1), (v // 60 or d + 2, v % 60))],
                   "1 日 ＝ 24 小時：%d ÷ 24 ＝ %d……%d。" % (v, d, h))
    return pick_unique(R, h2m, 5, seen) + pick_unique(R, m2h, 5, seen) + pick_unique(R, sec, 5, seen) + pick_unique(R, day, 5, seen)


def s2(seen):
    def add():
        a = R.randint(1, 3) * 60 + R.randint(1, 11) * 5
        b = R.randint(0, 2) * 60 + R.randint(1, 11) * 5
        if (a % 60 + b % 60) < 60 and R.random() < .6:
            return None
        s = a + b
        q = "%s ＋ %s ＝" % (du(a), du(b))
        w = ["%d 小時 %d 分鐘" % (a // 60 + b // 60, a % 60 + b % 60), du(s + 60), du(s - 60) if s > 60 else du(s + 120), du(s + 40)]
        return mcq(q, du(s), w, "分鐘加分鐘、小時加小時，滿 60 分鐘換成 1 小時：%s。" % du(s))

    def sub():
        a = R.randint(2, 5) * 60 + R.randint(0, 11) * 5
        b = R.randint(0, a // 60 - 1) * 60 + R.randint(1, 11) * 5
        d = a - b
        if d % 60 == 0:
            return None
        q = "%s － %s ＝" % (du(a), du(b))
        w = []
        if a % 60 < b % 60:
            w.append(hm(a // 60 - b // 60 - 1, a % 60 + 100 - b % 60))   # 1 小時を 100 分鐘として借りる
            w.append(hm(a // 60 - b // 60, b % 60 - a % 60))
        w += [du(d + 60), du(d - 60) if d > 60 else du(d + 120), du(d + 10), du(d - 5)]
        return mcq(q, du(d), w, "分鐘不夠減，向小時借 1 小時 ＝ 60 分鐘：%s。" % du(d))

    def sec():
        a = R.randint(2, 6) * 60 + R.randint(0, 59)
        b = R.randint(1, a // 60 - 1) * 60 + R.randint(1, 59)
        d = a - b
        if d % 60 == 0 or a % 60 >= b % 60:
            return None
        q = "%s － %s ＝" % (ds(a), ds(b))
        w = ["%d 分鐘 %d 秒" % (a // 60 - b // 60 - 1, a % 60 + 100 - b % 60), "%d 分鐘 %d 秒" % (a // 60 - b // 60, b % 60 - a % 60), ds(d + 60), ds(d + 1)]
        return mcq(q, ds(d), w, "秒不夠減，向分鐘借 1 分鐘 ＝ 60 秒：%s。" % ds(d))
    return pick_unique(R, add, 8, seen) + pick_unique(R, sub, 8, seen) + pick_unique(R, sec, 4, seen)


def s3(seen):
    def mk():
        t = R.randint(7 * 12, 19 * 12) * 5
        d = R.choice([R.randint(2, 11) * 5, R.randint(13, 47) * 5, R.randint(1, 3) * 60])
        if t % 60 == 0 and R.random() < .5:
            return None
        e = t + d
        if e > 21 * 60:
            return None
        q = "現在是%s，再過 %s是幾時幾分？" % (tm(t), du(d))
        if R.random() < .4:
            h = (t // 60) % 12 or 12
            q = "時鐘上是%s的時刻。再過 %s是幾時幾分？" % ("上午" if t < 720 else ("中午" if t < 780 else ("下午" if t < 1080 else "晚上")), du(d)) + clock(h, t % 60, 150)
        w = [tm(e + 60), tm(e - 60) if e - 60 > t else tm(e + 120), tm(e + 40) if (t % 60 + d % 60) >= 60 else tm(e + 10), tm(e - 5)]
        # 正午をまたぐのに「上午」のまま書く間違い
        if t < 720 <= e:
            w.insert(0, "上午 %d 時%s" % (e // 60, " %d 分" % (e % 60) if e % 60 else ""))
        return mcq(q, tm(e), w, "%s 再過 %s：%s。" % (tm(t), du(d), tm(e)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        t1 = R.randint(7 * 12, 18 * 12) * 5
        d = R.choice([R.randint(3, 11) * 5, R.randint(13, 59) * 5, R.randint(1, 5) * 60])
        t2 = t1 + d
        if t2 > 21 * 60:
            return None
        who = NM.next()
        act = R.choice(["看書", "練鋼琴", "去圖書館", "上才藝課", "去公園玩", "做功課"])
        q = "%s從%s開始%s，到%s結束，一共經過多久？" % (who, tm(t1), act, tm(t2))
        w = []
        if t2 % 60 < t1 % 60:
            w.append(du((t2 // 60 - t1 // 60 - 1) * 60 + (t2 % 60 + 100 - t1 % 60)) if (t2 % 60 + 100 - t1 % 60) < 60 else hm(t2 // 60 - t1 // 60 - 1, t2 % 60 + 100 - t1 % 60))
            w.append(hm(t2 // 60 - t1 // 60, t1 % 60 - t2 % 60))
        if t1 < 720 < t2:
            h2 = (t2 // 60) % 12 or 12
            if t1 // 60 > h2:
                w.append(du((t1 // 60 - h2) * 60 + abs(t2 % 60 - t1 % 60)))
        w += [du(d + 60), du(d - 60) if d > 60 else du(d + 120), du(d + 10), du(d - 5)]
        return mcq(q, du(d), w, "從%s到%s：%s。" % (tm(t1), tm(t2), "；".join(steps(t1, t2))))
    return pick_unique(R, mk, 20, seen)


def steps(t1, t2):
    """經過時間の考え方：次の整點まで → 整點から整點 → 最後の分"""
    out = []
    if t1 % 60 and t2 // 60 > t1 // 60:
        nxt = (t1 // 60 + 1) * 60
        out.append("到%s是 %d 分鐘" % (tm(nxt), nxt - t1))
        if t2 >= nxt + 60:
            out.append("再到%s是 %d 小時" % (tm(t2 // 60 * 60), (t2 // 60 * 60 - nxt) // 60)) if t2 // 60 * 60 > nxt else None
        if t2 % 60:
            out.append("再 %d 分鐘" % (t2 % 60))
        out.append("合起來 %s" % du(t2 - t1))
    else:
        out.append("一共 %s" % du(t2 - t1))
    return [o for o in out if o]


def s5(seen):
    SENSE = [("跑 50 公尺", "10", "秒"), ("刷牙", "3", "分鐘"), ("晚上睡覺", "9", "小時"), ("放完一個暑假", "60", "日"),
             ("一節數學課", "40", "分鐘"), ("眨一下眼睛", "1", "秒"), ("看一部卡通電影", "2", "小時"), ("吃一頓午餐", "20", "分鐘")]
    out = []
    for it, n, u in SENSE:
        out.append(mcq("%s大約要 %s ___，填哪一個單位最合適？" % (it, n), u, [x for x in ("秒", "分鐘", "小時", "日") if x != u],
                       "想一想實際要多久：%s大約 %s %s。" % (it, n, u)))
    for b in out:
        seen.add(b["q"])

    def word():
        who = NM.next()
        kind = R.choice(["movie", "train", "class"])
        if kind == "movie":
            t = R.choice([13, 14, 15, 18, 19]) * 60 + R.choice([0, 10, 20, 30, 40])
            d = R.choice([95, 100, 110, 115, 125])
            q = "電影%s開始，片長 %s。電影幾時幾分結束？" % (tm(t), du(d))
            e = t + d
            return mcq(q, tm(e), [tm(e + 40) if (t % 60 + d % 60) >= 60 else tm(e + 60), tm(e - 60), tm(t + d % 60), tm(e + 10)], "%s 再過 %s 是%s。" % (tm(t), du(d), tm(e)))
        if kind == "train":
            t1 = R.choice([7, 8, 9, 10]) * 60 + R.choice([5, 15, 25, 35, 45, 55])
            d = R.randint(5, 23) * 10
            t2 = t1 + d
            q = "%s搭火車，%s出發，%s到達。坐了多久的火車？" % (who, tm(t1), tm(t2))
            return mcq(q, du(d), [du(d + 60), du(d + 40) if (t2 % 60) < (t1 % 60) else du(d + 10), du(d - 10), du(d + 20)],
                       "從%s到%s，經過 %s。" % (tm(t1), tm(t2), du(d)))
        n = R.randint(3, 6)
        m = R.choice([35, 40, 45])
        q = "每節課 %d 分鐘，%s今天上了 %d 節課，一共上了多久？（用幾小時幾分鐘回答）" % (m, who, n)
        v = m * n
        return mcq(q, du(v), [du(v + 40) if v % 60 else du(v + 20), "%d 小時 %d 分鐘" % (v // 100, v % 100) if v % 100 and v // 100 else du(v + 60), du(v - 60), du(v + 60)],
                   "%d × %d ＝ %d（分鐘）＝ %s。" % (m, n, v, du(v)))
    return out + pick_unique(R, word, 12, seen)


def main():
    seen = set()
    sets = [("時間單位的換算", s1(seen)), ("時間量的加減", s2(seen)), ("再過多久是幾時幾分", s3(seen)),
            ("經過多久", s4(seen)), ("量感和應用問題", s5(seen))]
    body = lesson(
        ["<b>1 日 ＝ 24 小時</b>，<b>1 小時 ＝ 60 分鐘</b>，<b>1 分鐘 ＝ 60 秒</b>。",
         "時間是 <b>60 進位</b>：分鐘滿 60 換成 1 小時；不夠減時，借 1 小時是 60 分鐘（不是 100）。",
         "算經過多久：先算到下一個整點，再算整點到整點，最後加上剩下的分鐘。",
         "過了中午 12 時，就是下午 1 時、2 時……。"],
        [example("上午 9 時 40 分再過 35 分鐘是幾時幾分？", ["40 分 ＋ 35 分 ＝ 75 分。", "75 分 ＝ 1 小時 15 分，9 時變 10 時。"], "上午 10 時 15 分"),
         example("從上午 8 時 20 分到上午 10 時 5 分，經過多久？", ["8 時 20 分到 9 時：40 分鐘。", "9 時到 10 時：1 小時。再 5 分鐘。"], "1 小時 45 分鐘")],
        [("2 小時 15 分鐘 ＝ 215 分鐘", "1 小時 ＝ 60 分鐘：120 ＋ 15 ＝ 135 分鐘"),
         ("3 時 10 分 － 1 時 45 分 ＝ 1 時 65 分", "借 1 小時是 60 分鐘：70 － 45 ＝ 25，答案 1 小時 25 分鐘"),
         ("上午 10 時到下午 2 時是 8 小時（10 － 2）", "到中午 12 時是 2 小時，再到下午 2 時是 2 小時，共 4 小時")])
    faq = [{"q": "三年級的時間單元要學什麼？",
            "a": "108課綱 N-3-17：認識日、時、分、秒，做時間單位的換算，並解決「再過多久是幾時」「經過多久」等時間加減問題。"},
           {"q": "「時」和「小時」有什麼不同？",
            "a": "「上午 9 時」是時刻（時鐘上的某一刻）；「2 小時」是時間量（經過了多久）。課本常用「時刻」和「時間量」來區分。"},
           {"q": "孩子算時間常用 100 去借位，怎麼辦？",
            "a": "提醒時間是 60 進位：1 小時 ＝ 60 分鐘。可以畫時間線，先算到整點，再一段一段加起來。"}]
    make_unit(R, "grade-3", "time", "N-3-17",
              "時間：「日」、「時」、「分」、「秒」。實測、量感、估測與計算。時間單位的換算。認識時間加減問題的類型。",
              "時間：日、時、分、秒的換算與計算",
              "三年級數學 時間 練習題｜時間換算・經過多久・再過多久 學習單（附解答）",
              "時間（日時分秒）",
              "國小三年級數學「時間」免費學習單：日、小時、分鐘、秒的換算，時間量的加減，再過多久是幾時幾分，經過多久和生活應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 小時 ＝ 60 分鐘，1 分鐘 ＝ 60 秒",
              "時間是 60 進位：滿 60 進 1，借 1 小時是 60 分鐘。",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
