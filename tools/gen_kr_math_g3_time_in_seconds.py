# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：초 단위까지의 시각과 시간의 덧셈과 뺄셈（2022 개정 [4수03-13] [4수03-14]）
誤答は「1분 = 100초」「60초를 받아올림하지 않는다」「받아내림을 100으로 한다」「초바늘の숫자をそのまま초で読む」から作る。
"""
import random
from kr_common import mcq, unit, Names, josa, clock

R = random.Random(82307)
NM = Names(R)


def hms(h, m, s):
    t = "%d시" % h
    if m:
        t += " %d분" % m
    if s:
        t += " %d초" % s
    return t


def dur(sec):
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    out = []
    if h:
        out.append("%d시간" % h)
    if m:
        out.append("%d분" % m)
    if s:
        out.append("%d초" % s)
    return " ".join(out) if out else "0초"


def read_clock():
    h, m, s = R.randint(1, 12), R.randint(0, 59), R.randrange(5, 60, 5)
    if s == 0:
        return None
    f = clock(h, m, sec=s, label="시계 %d시 %d분 %d초" % (h, m, s))
    ans = hms(h, m, s)
    w = [hms(h, m, s // 5), hms(h, (m + 1) % 60, s), hms(h, m, (s + 5) % 60 or 10), hms(h % 12 + 1, m, s)]
    return mcq(f + "빨간 초바늘이 있는 시계예요. 몇 시 몇 분 몇 초인가요?", ans, [x for x in w if x != ans],
               "초바늘이 가리키는 숫자가 %d이면 %d × 5 = %d초예요. <b>%s</b>" % (s // 5, s // 5, s, ans))


def convert():
    k = R.choice(["m2s", "s2m", "ms2s"])
    if k == "m2s":
        m = R.randint(2, 9)
        return mcq("%d분은 몇 초인가요?" % m, "%d초" % (m * 60), ["%d초" % x for x in (m * 100, m * 10, m * 60 + 60, m + 60)],
                   "1분 = 60초예요. %d분 = 60 × %d = <b>%d초</b>" % (m, m, m * 60))
    if k == "s2m":
        m, s = R.randint(1, 5), R.randint(1, 59)
        t = m * 60 + s
        return mcq("%d초는 몇 분 몇 초인가요?" % t, dur(t), [dur(t + 40) if (t + 40) % 60 else dur(t + 41), "%d분 %d초" % (t // 100, t % 100) if t >= 100 else "%d분 %d초" % (m + 1, s),
                                                              "%d분 %d초" % (m, s + 1) if s < 59 else "%d분" % (m + 1), dur(t - 60) if t > 60 else dur(t + 60)],
                   "60초 = 1분이에요. %d초 = %d초 + %d초 = <b>%s</b>" % (t, m * 60, s, dur(t)))
    m, s = R.randint(1, 6), R.randint(5, 55)
    t = m * 60 + s
    return mcq("%d분 %d초는 몇 초인가요?" % (m, s), "%d초" % t, ["%d초" % x for x in (m * 100 + s, m + s, t + 60, m * 10 + s)],
               "%d분 = %d초이니까 %d + %d = <b>%d초</b>" % (m, m * 60, m * 60, s, t))


def add_time(carry=True):
    def mk():
        h, m, s = R.randint(1, 10), R.randint(5, 50), R.randint(5, 55)
        dm, ds = R.randint(1, 40), R.randint(5, 55)
        if carry != (s + ds >= 60):
            return None
        t = (h * 3600 + m * 60 + s) + dm * 60 + ds
        H, r = divmod(t, 3600)
        M, S = divmod(r, 60)
        if H > 12:
            return None
        ans = hms(H, M, S)
        nc = hms(h + (m + dm) // 60, (m + dm) % 60, (s + ds) % 100) if (s + ds) < 100 else hms(H, M, S + 1)
        w = [nc, hms(H, (M + 1) % 60, S), hms(H, M - 1 if M else 59, S), hms(H + 1, M, S)]
        return mcq("%s + %s =" % (hms(h, m, s), dur(dm * 60 + ds)), ans, [x for x in w if x != ans],
                   "초는 초끼리, 분은 분끼리 더해요. 60초가 넘으면 <b>1분으로 받아올림</b>해요. <b>%s</b>" % ans)
    return mk


def sub_time(borrow=True):
    def mk():
        h, m, s = R.randint(2, 11), R.randint(5, 55), R.randint(0, 50)
        dm, ds = R.randint(1, 40), R.randint(5, 55)
        if borrow != (ds > s):
            return None
        t = (h * 3600 + m * 60 + s) - (dm * 60 + ds)
        H, r = divmod(t, 3600)
        M, S = divmod(r, 60)
        ans = hms(H, M, S)
        w = [hms(H, M, (s + 100 - ds) % 100) if borrow else hms(H, M, S + 1), hms(H, (M + 1) % 60, S), hms(H, M, ds - s if borrow else S + 10), hms(H - 1 if H > 1 else 12, M, S)]
        return mcq("%s − %s =" % (hms(h, m, s), dur(dm * 60 + ds)), ans, [x for x in w if x != ans],
                   "초는 초끼리, 분은 분끼리 빼요. 초끼리 뺄 수 없으면 <b>1분을 60초로 받아내림</b>해요. <b>%s</b>" % ans)
    return mk


def elapsed():
    h, m, s = R.randint(1, 10), R.randint(0, 50), R.randint(0, 55)
    d = R.randint(70, 2400)
    t0 = h * 3600 + m * 60 + s
    t1 = t0 + d
    H, r = divmod(t1, 3600)
    M, S = divmod(r, 60)
    ans = dur(d)
    w = [dur(d + 60), dur(d - 60) if d > 60 else dur(d + 120), dur(d + 40) if (d + 40) % 60 else dur(d + 41), dur(d + 1)]
    return mcq("시작한 시각은 %s, 끝난 시각은 %s예요. 걸린 시간은 얼마인가요?" % (hms(h, m, s), hms(H, M, S)), ans, [x for x in w if x != ans],
               "끝난 시각 − 시작한 시각을 계산해요. 초끼리 뺄 수 없으면 1분 = 60초로 받아내림해요. <b>%s</b>" % ans)


def story():
    who = NM.next()
    k = R.choice(["run", "start", "end", "song"])
    if k == "run":
        a, b = R.randint(50, 170), R.randint(50, 170)
        t = "%s 운동장을 한 바퀴 도는 데 %s, 두 바퀴째에는 %s가 걸렸어요. 두 바퀴를 도는 데 걸린 시간은 모두 얼마인가요?" % (josa(who, "은/는"), dur(a), dur(b))
        ans = dur(a + b)
        w = [dur(a + b + 60), dur(abs(a - b)) if a != b else dur(a + b - 1), dur(a + b + 40) if (a + b + 40) % 60 else dur(a + b + 41), dur(a + b - 60) if a + b > 60 else dur(a + b + 2)]
    elif k == "start":
        h, m = R.randint(1, 5), R.randint(5, 55)
        d = R.randint(20, 59) * 60 + R.randint(5, 55)
        t1 = h * 3600 + m * 60 + d
        H, r = divmod(t1, 3600)
        M, S = divmod(r, 60)
        t = "%s 오후 %s에 숙제를 시작해서 %s 동안 했어요. 숙제를 끝낸 시각은 오후 몇 시 몇 분 몇 초인가요?" % (josa(who, "은/는"), hms(h, m, 0), dur(d))
        ans = "오후 " + hms(H, M, S)
        w = ["오후 " + hms(H, (M + 1) % 60, S), "오후 " + hms(H + 1, M, S), "오후 " + hms(H, M - 1 if M else 59, S)]
    elif k == "song":
        a = R.randint(150, 270)
        b = R.randint(150, 270)
        t = "노래 두 곡의 길이는 %s와 %s예요. 두 곡을 이어서 들으면 모두 얼마나 걸리나요?" % (dur(a), dur(b))
        ans = dur(a + b)
        w = [dur(a + b + 60), dur(a + b - 60), dur(a + b + 40) if (a + b + 40) % 60 else dur(a + b + 41), dur(abs(a - b)) if a != b else dur(a + b + 1)]
    else:
        r1 = R.randint(15, 25)
        x = R.randint(1, 6)
        fr = NM.next()
        t = "100 m 달리기에서 %s 기록은 %d초, %s 기록은 %d초예요. %s %s보다 몇 초 더 빨리 달렸나요?" % (who + "의", r1, fr + "의", r1 + x, josa(who, "이/가"), fr)
        ans = "%d초" % x
        w = ["%d초" % (x + 1), "%d초" % (2 * r1 + x), "%d초" % (x + 10)]
    return mcq(t, ans, [y for y in w if y != ans], "시간끼리 더하거나 빼요. 60초는 1분, 60분은 1시간으로 받아올림해요. <b>%s</b>" % ans)


unit("grade-3", "time-in-seconds", 7, "[4수03-13] [4수03-14]",
     "1분과 1초의 관계를 이해하고, 초 단위까지 시각을 읽을 수 있다. 실생활 문제 상황과 연결하여 초 단위까지의 시간의 덧셈과 뺄셈을 할 수 있다.",
     "초 단위까지의 시각과 시간 계산", "시간 (초 단위)",
     "초등 3학년 시간 학습지: 초바늘 읽기, 분과 초 바꾸기, 시각과 시간의 덧셈과 뺄셈, 걸린 시간 구하기, 문장제까지 100문제와 정답.",
     "1분 = 60초, 1시간 = 60분", "60이 되면 받아올림, 모자라면 60을 받아내림해요.",
     ["초바늘이 작은 눈금 한 칸을 가는 동안 걸린 시간은 <b>1초</b>예요. 초바늘이 한 바퀴 돌면 <b>60초 = 1분</b>이에요.",
      "초바늘이 숫자 3을 가리키면 15초, 숫자 7을 가리키면 35초예요(숫자 × 5).",
      "시간을 더하고 뺄 때는 <b>초는 초끼리, 분은 분끼리, 시는 시끼리</b> 계산해요.",
      "초끼리 더해서 60이 넘으면 1분으로 받아올림하고, 뺄 수 없으면 1분을 60초로 받아내림해요. 100이 아니라 <b>60</b>이에요."],
     [("2시 40분 35초 + 15분 40초 =", ["초: 35 + 40 = 75초 = 1분 15초", "분: 40 + 15 + 1 = 56분"], "2시 56분 15초"),
      ("5시 20분 10초 − 3분 45초 =", ["초: 10초에서 45초를 뺄 수 없어요. 1분 = 60초를 받아내림: 70 − 45 = 25", "분: 19 − 3 = 16"], "5시 16분 25초")],
     [("1분을 100초로 생각한다", "1분 = 60초예요. 받아올림, 받아내림도 60으로 해요."),
      ("초바늘이 4를 가리키면 4초라고 읽는다", "숫자 한 칸은 5초예요. 4를 가리키면 20초예요."),
      ("시각과 시각을 더한다", "시각 + 시각은 뜻이 없어요. 시각 + 시간 = 시각, 시각 − 시각 = 시간이에요.")],
     [("초 단위 시간 계산은 언제 배우나요?", "초등 3학년 1학기 「길이와 시간」 단원에서 배워요. 2학년에서 배운 시각과 시간을 초까지 넓혀요."),
      ("시각과 시간은 어떻게 다른가요?", "시각은 「3시 20분」처럼 어느 한 때를 말하고, 시간은 「20분 동안」처럼 시각과 시각 사이의 길이를 말해요.")],
     [("초 단위까지 시각 읽기", [(read_clock, 20)]),
      ("분과 초 바꾸기", [(convert, 20)]),
      ("시간의 덧셈", [(add_time(False), 8), (add_time(True), 12)]),
      ("시간의 뺄셈과 걸린 시간", [(sub_time(False), 6), (sub_time(True), 8), (elapsed, 6)]),
      ("문장제", [(story, 20)])],
     82307)
