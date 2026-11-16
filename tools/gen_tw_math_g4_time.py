# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：時間的計算（24 小時制、跨午、跨日）（108課綱 N-4-13）
  python3 tools/gen_tw_math_g4_time.py
12 時制⇔24 時制、時間單位の換算（日・時・分・秒）、經過時間（跨時・跨午・跨日）、開始・結束時刻、應用（時刻表・營業時間）。
誤答：下午 3 時を 3 時のまま、跨午で 12 を足し忘れ、跨日で 24 を足し忘れ、60 進位でなく 100 で借りる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names

R = random.Random(41015)
NM = Names(R)


def t12(t):
    h, m = divmod(t % 1440, 60)
    if h < 12:
        p = "凌晨" if h < 5 else "上午"
        hh = h if h else 12
        if h == 0:
            p = "半夜"
    elif h == 12:
        p, hh = "中午", 12
    else:
        p, hh = ("下午" if h < 18 else "晚上"), h - 12
    return "%s %d 時%s" % (p, hh, " %d 分" % m if m else "")


def t24(t):
    h, m = divmod(t % 1440, 60)
    return "%02d:%02d" % (h, m)


def du(m):
    a, b = divmod(m, 60)
    if a and b:
        return "%d 小時 %d 分鐘" % (a, b)
    return "%d 小時" % a if a else "%d 分鐘" % b


def hm(a, b):
    return "%d 分鐘" % b if a == 0 else "%d 小時 %d 分鐘" % (a, b)


def s1(seen):
    def to24():
        t = R.randint(13 * 12, 23 * 12) * 5 if R.random() < .7 else R.randint(1 * 12, 11 * 12) * 5
        q = "%s，用 24 小時制怎麼表示？" % t12(t)
        h, m = divmod(t, 60)
        w = ["%02d:%02d" % (h - 12 if h > 12 else h + 12, m), "%02d:%02d" % (h, (m + 10) % 60), "%02d:%02d" % ((h + 1) % 24, m), "%02d:%02d" % (h + 2 if h < 22 else h - 2, m)]
        return mcq(q, t24(t), w, "%s%s。" % ("下午、晚上的時刻要加 12：%d ＋ 12 ＝ %d，" % (h - 12, h) if h > 12 else "上午的時刻不變，", "寫成 " + t24(t)))

    def to12():
        t = R.randint(13 * 12, 23 * 12 + 11) * 5
        h, m = divmod(t, 60)
        q = "%s 是 12 小時制的什麼時刻？" % t24(t)
        w = ["上午 %d 時%s" % (h - 12, " %d 分" % m if m else ""), t12(t + 60), t12(t - 120), "下午 %d 時%s" % (h, " %d 分" % m if m else "")]
        return mcq(q, t12(t), w, "超過 12 要減 12：%d － 12 ＝ %d，是%s。" % (h, h - 12, t12(t)))
    return pick_unique(R, to24, 10, seen) + pick_unique(R, to12, 10, seen)


def s2(seen):
    def mk():
        kind = R.choice(["d2h", "h2d", "h2m", "m2s", "s2m"])
        if kind == "d2h":
            d, h = R.randint(1, 5), R.randint(1, 23)
            v = d * 24 + h
            return mcq("%d 日 %d 小時 ＝ ___ 小時" % (d, h), str(v), [str(x) for x in (d * 12 + h, d * 60 + h, d * 100 + h, v + 24)], "1 日 ＝ 24 小時：%d × 24 ＋ %d ＝ %d。" % (d, h, v))
        if kind == "h2d":
            v = R.randint(25, 150)
            d, h = divmod(v, 24)
            if h == 0:
                return None
            return mcq("%d 小時 ＝ ___ 日 ___ 小時" % v, "%d 日 %d 小時" % (d, h), ["%d 日 %d 小時" % x for x in ((v // 12, v % 12), (v // 60 if v >= 60 else d + 1, v % 60), (d + 1, h), (d - 1, h + 24) if d > 1 else (d, h + 1))],
                       "%d ÷ 24 ＝ %d……%d。" % (v, d, h))
        if kind == "h2m":
            a, b = R.randint(2, 9), R.randint(5, 55)
            v = a * 60 + b
            return mcq("%d 小時 %d 分鐘 ＝ ___ 分鐘" % (a, b), str(v), [str(x) for x in (a * 100 + b, a + b, v + 60, v - 60)], "%d × 60 ＋ %d ＝ %d。" % (a, b, v))
        if kind == "m2s":
            a, b = R.randint(2, 15), R.randint(5, 55)
            v = a * 60 + b
            return mcq("%d 分鐘 %d 秒 ＝ ___ 秒" % (a, b), str(v), [str(x) for x in (a * 100 + b, a + b, v + 60, v - 60)], "%d × 60 ＋ %d ＝ %d。" % (a, b, v))
        v = R.randint(130, 900)
        a, b = divmod(v, 60)
        if b == 0:
            return None
        return mcq("%d 秒 ＝ ___ 分鐘 ___ 秒" % v, "%d 分鐘 %d 秒" % (a, b), ["%d 分鐘 %d 秒" % x for x in ((v // 100, v % 100) if v % 100 < 60 else (a + 1, b), (a + 1, b), (a - 1, b + 60), (a, 60 - b) if 60 - b != b else (a, b + 1))],
                   "%d ÷ 60 ＝ %d……%d。" % (v, a, b))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def noon():
        t1 = R.randint(8 * 12, 11 * 12 + 11) * 5
        t2 = R.randint(12 * 12 + 1, 18 * 12) * 5
        d = t2 - t1
        q = "從%s到%s，經過多久？" % (t12(t1), t12(t2))
        h1, h2 = t1 // 60, t2 // 60 - 12
        w = [hm(abs(h2 - h1), abs(t2 % 60 - t1 % 60)) if h2 != h1 else du(d + 60), du(d + 60), du(d - 60) if d > 60 else du(d + 120), du(d + 10)]
        return mcq(q, du(d), [x for x in w if x != du(d)] + [du(d - 10)], "用 24 小時制：%s 到 %s，經過 %s。" % (t24(t1), t24(t2), du(d)))

    def night():
        t1 = R.randint(19 * 12, 23 * 12) * 5
        t2 = R.randint(5 * 12, 8 * 12) * 5 + 1440
        d = t2 - t1
        q = "從%s到第二天%s，經過多久？" % (t12(t1), t12(t2))
        w = [du(abs(t1 - (t2 - 1440)) - 720) if abs(t1 - (t2 - 1440)) > 720 else du(d - 120), du(d + 60), du(d - 60), du(abs((t2 - 1440) - (t1 - 720)))]
        return mcq(q, du(d), [x for x in w if x != du(d)] + [du(d + 120)], "到半夜 12 時是 %s，再到%s是 %s，一共 %s。" % (du(1440 - t1), t12(t2), du(t2 - 1440), du(d)))
    return pick_unique(R, noon, 10, seen) + pick_unique(R, night, 10, seen)


def s4(seen):
    def end():
        t = R.randint(7 * 12, 20 * 12) * 5
        d = R.choice([R.randint(13, 47) * 5, R.randint(1, 5) * 60 + R.randint(1, 11) * 5])
        e = t + d
        if e >= 1440:
            return None
        q = "%s 開始，經過 %s，結束時是幾時幾分？（用 24 小時制回答）" % (t24(t), du(d))
        w = [t24(e + 60), t24(e - 60), t24(e + 40) if (t % 60 + d % 60) >= 60 else t24(e + 10), t24(e - 5)]
        return mcq(q, t24(e), w, "%s 再過 %s：%s。" % (t24(t), du(d), t24(e)))

    def start():
        e = R.randint(10 * 12, 22 * 12) * 5
        d = R.choice([R.randint(13, 47) * 5, R.randint(1, 4) * 60 + R.randint(1, 11) * 5])
        t = e - d
        q = "活動在 %s 結束，一共進行了 %s，是幾時幾分開始的？（用 24 小時制回答）" % (t24(e), du(d))
        w = [t24(e + d), t24(t + 60), t24(t - 60), t24(t + 40) if e % 60 < d % 60 else t24(t + 10)]
        return mcq(q, t24(t), w, "往前推：%s 往前 %s 是 %s。" % (t24(e), du(d), t24(t)))
    return pick_unique(R, end, 10, seen) + pick_unique(R, start, 10, seen)


def s5(seen):
    def train():
        t1 = R.randint(6 * 12, 20 * 12) * 5
        st, lo, hi = R.choice([(("台北", "台中"), 50, 65), (("台北", "高雄"), 95, 120), (("新竹", "台南"), 65, 85), (("台中", "高雄"), 45, 60), (("台北", "台南"), 85, 110)])
        d = R.randint(lo // 5, hi // 5) * 5
        t2 = t1 + d
        if t2 >= 1440:
            return None
        q = "高鐵 %s 從%s出發，%s 到達%s，車程多久？" % (t24(t1), st[0], t24(t2), st[1])
        w = [hm(t2 // 60 - t1 // 60, abs(t2 % 60 - t1 % 60)) if t2 % 60 < t1 % 60 else du(d + 60), du(d + 60), du(d - 10), du(d + 10)]
        return mcq(q, du(d), [x for x in w if x != du(d)] + [du(d + 40)], "%s 到 %s，經過 %s。" % (t24(t1), t24(t2), du(d)))

    def shop():
        o = R.randint(7, 11) * 60 + R.choice([0, 30])
        c = R.randint(20, 23) * 60 + R.choice([0, 30])
        d = c - o
        q = "一家商店營業時間是 %s 到 %s，一天營業幾小時？" % (t24(o), t24(c))
        w = [du(d - 60), du(d + 60), du(abs(c // 60 - 12 - o // 60) * 60 + abs(c % 60 - o % 60)) if c // 60 - 12 != o // 60 else du(d + 120), du(d + 30)]
        return mcq(q, du(d), [x for x in w if x != du(d)], "%s 到 %s：%s。" % (t24(o), t24(c), du(d)))

    def sleep():
        b = R.randint(20 * 12 + 6, 22 * 12 + 6) * 5
        w_ = R.randint(6 * 12, 7 * 12) * 5 + 1440
        d = w_ - b
        who = NM.next()
        q = "%s晚上 %s 睡覺，第二天早上 %s 起床，睡了多久？" % (who, t24(b), t24(w_))
        w = [du(abs(b - (w_ - 1440)) - 720) if abs(b - (w_ - 1440)) > 720 else du(d + 60), du(d + 60), du(d - 60), du(abs((b - 720) - (w_ - 1440)))]
        return mcq(q, du(d), [x for x in w if x != du(d)] + [du(d + 30)], "到 24:00 是 %s，再到 %s 是 %s，一共 %s。" % (du(1440 - b), t24(w_), du(w_ - 1440), du(d)))
    return pick_unique(R, train, 8, seen) + pick_unique(R, shop, 6, seen) + pick_unique(R, sleep, 6, seen)


def main():
    seen = set()
    sets = [("12 小時制和 24 小時制", s1(seen)), ("時間單位的換算", s2(seen)), ("跨午、跨日經過多久", s3(seen)),
            ("開始和結束的時刻", s4(seen)), ("生活中的時間", s5(seen))]
    body = lesson(
        ["<b>24 小時制</b>：下午和晚上的時刻要 ＋12。下午 3 時 ＝ 15:00，晚上 8 時 30 分 ＝ 20:30。",
         "1 日 ＝ 24 小時，1 小時 ＝ 60 分鐘，1 分鐘 ＝ 60 秒。借 1 小時是 60 分鐘，不是 100。",
         "算經過多久：先換成 24 小時制再相減。跨過半夜時，先算到 24:00，再加上第二天的時間。"],
        [example("從上午 10 時 40 分到下午 2 時 15 分，經過多久？", ["換成 24 小時制：10:40 到 14:15。", "10:40 到 14:40 是 4 小時，再往回 25 分鐘。"], "3 小時 35 分鐘"),
         example("晚上 9 時睡到第二天早上 6 時 30 分，睡了多久？", ["21:00 到 24:00 是 3 小時。", "0:00 到 6:30 是 6 小時 30 分鐘。"], "9 小時 30 分鐘")],
        [("下午 3 時寫成 03:00", "下午要 ＋12：15:00"),
         ("上午 10 時到下午 2 時是 8 小時（10 － 2）", "換成 24 小時制：14 － 10 ＝ 4 小時"),
         ("借位時借 100 分鐘", "1 小時只有 60 分鐘")])
    faq = [{"q": "24 小時制怎麼換？",
            "a": "上午（凌晨）的時刻數字不變；下午、晚上的時刻加 12。例如晚上 7 時 ＝ 19:00，19:00 減 12 就是 12 小時制的晚上 7 時。"},
           {"q": "跨日的經過時間怎麼算？",
            "a": "先算到半夜 24:00 有多久，再加上第二天 0:00 到結束時刻的時間。例如 22:00 到第二天 7:00：2 小時 ＋ 7 小時 ＝ 9 小時。"},
           {"q": "四年級的時間要學什麼？",
            "a": "108課綱 N-4-13：日常生活的時間加減問題，包含跨時、跨午、跨日、24 小時制和時間單位的換算。"}]
    make_unit(R, "grade-4", "time", "N-4-13",
              "解題：日常生活的時間加減問題。跨時、跨午、跨日、24 小時制。含時間單位換算。",
              "時間的計算：24 小時制、跨午、跨日",
              "四年級數學 時間計算 練習題｜24小時制・跨日・經過時間 學習單（附解答）",
              "時間的計算",
              "國小四年級數學「時間的計算」免費學習單：12小時制和24小時制、時間單位換算、跨午和跨日的經過時間、開始和結束時刻與生活應用題。100題線上練習馬上對答案，附可列印解答。",
              "下午、晚上的時刻 ＋12",
              "跨日：先算到 24:00，再加上第二天的時間。",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
