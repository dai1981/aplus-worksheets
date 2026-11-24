# -*- coding: utf-8 -*-
"""
대한민국 초등 3학년 수학：1 mm와 1 km（2022 개정 [4수03-15] [4수03-16]）
자로 몇 cm 몇 mm 재기、cm ↔ mm、km ↔ m、길이 어림하기、길이의 덧셈과 뺄셈。
誤答は「1 km = 100 m」「1 cm = 100 mm」「자의 0이 아닌 곳から재고 끝の눈금を読む」から作る。
"""
import random
from kr_common import mcq, num, unit, Names, josa
from kr_pics import ruler

R = random.Random(82306)
NM = Names(R)


def cmmm(mm):
    c, m = divmod(mm, 10)
    if c and m:
        return "%d cm %d mm" % (c, m)
    return "%d cm" % c if c else "%d mm" % m


def kmm(m):
    k, r = divmod(m, 1000)
    if k and r:
        return "%d km %d m" % (k, r)
    return "%d km" % k if k else "%d m" % r


def measure():
    start = R.choice([0, 0, 10, 20, 30])
    ln = R.randint(15, 95)
    if ln % 10 == 0:
        return None
    end = start + ln
    obj = R.choice(["연필", "지우개", "클립", "색연필", "크레파스", "막대"])
    f = ruler(start, end, max(end // 10 + 2, 8), obj)
    q = f + "%s의 길이는 몇 cm 몇 mm인가요?" % obj
    w = [cmmm(end), cmmm(ln + 10), cmmm(ln - 1), "%d cm %d mm" % (ln % 10, ln // 10)]
    e = "작은 눈금 한 칸은 1 mm예요. " + ("0에서 시작하니까 끝의 눈금을 읽어요." if start == 0 else "%d에서 시작하니까 %d cm를 빼요." % (start // 10, start // 10))
    return mcq(q, cmmm(ln), [x for x in w if x != cmmm(ln)], e + " <b>%s</b>" % cmmm(ln))


def to_mm():
    c, m = R.randint(1, 25), R.randint(1, 9)
    mm = c * 10 + m
    if R.random() < 0.5:
        return mcq("%d cm %d mm는 몇 mm인가요?" % (c, m), "%d mm" % mm, ["%d mm" % x for x in (c * 100 + m, c + m, c * 10, mm + 10)],
                   "1 cm = 10 mm이니까 %d cm = %d mm예요. %d + %d = <b>%d</b>(mm)" % (c, c * 10, c * 10, m, mm))
    return mcq("%d mm는 몇 cm 몇 mm인가요?" % mm, "%d cm %d mm" % (c, m), ["%d cm %d mm" % (m, c), "%d cm %d mm" % (c + 1, m), "%d cm" % mm, "%d cm %d mm" % (c, (m + 1) % 10 or 2)],
                   "10 mm = 1 cm예요. %d mm = %d mm + %d mm = <b>%d cm %d mm</b>" % (mm, c * 10, m, c, m))


def to_m():
    k, m = R.randint(1, 9), R.randint(1, 999)
    if m % 100 == 0:
        return None
    t = k * 1000 + m
    if R.random() < 0.5:
        return mcq("%d km %d m는 몇 m인가요?" % (k, m), "%s m" % num(t), ["%s m" % num(x) for x in (k * 100 + m, k + m, k * 10000 + m, k * 1000 + m * 10)],
                   ("1 km = 1000 m예요. " if k == 1 else "1 km = 1000 m이니까 %d km = %d m예요. " % (k, k * 1000)) + "%d + %d = <b>%s</b>(m)" % (k * 1000, m, num(t)))
    return mcq("%s m는 몇 km 몇 m인가요?" % num(t), kmm(t), [kmm(t + 1000), "%d km %d m" % (t // 100, t % 100), "%d km %d m" % (k, m * 10) if m < 100 else kmm(t - 1000 if t > 2000 else t + 2000)],
               "1000 m = 1 km예요. %s m = %d m + %d m = <b>%s</b>" % (num(t), k * 1000, m, kmm(t)))


def compare_cm():
    if True:
        a = R.randint(21, 98)
        b = a + R.choice([-3, -1, 1, 4])
        if b % 10 == 0 or a % 10 == 0:
            return None
        A, B = cmmm(a), "%d mm" % b
        big = A if a > b else B
        return mcq("더 긴 것은? %s, %s" % (A, B), big, [B if big == A else A, "길이가 같아요", "알 수 없어요"],
                   "단위를 같게 바꾸어 비교해요. %s = %d mm, %d mm이니까 <b>%s</b>가 더 길어요." % (A, a, b, big))


def compare_km():
    a = R.randint(1100, 8900)
    b = a + R.choice([-90, -10, 20, 300])
    if a % 100 == 0:
        return None
    A, B = kmm(a), "%s m" % num(b)
    big = A if a > b else B
    return mcq("더 먼 거리는? %s, %s" % (A, B), big, [B if big == A else A, "거리가 같아요", "알 수 없어요"],
               "단위를 같게 바꾸어 비교해요. %s = %s m, %s m이니까 <b>%s</b>가 더 멀어요." % (A, num(a), num(b), big))


EST = [("운동장 한 바퀴", "200 m", ["200 km", "200 cm", "200 mm"]), ("서울에서 부산까지의 거리", "400 km", ["400 m", "400 cm", "40 m"]),
       ("공책의 두께", "3 mm", ["3 cm", "3 m", "30 cm"]), ("교과서의 긴 쪽 길이", "26 cm", ["26 mm", "26 m", "26 km"]),
       ("동전 하나의 두께", "2 mm", ["2 cm", "2 m", "20 cm"]), ("학교 건물의 높이", "15 m", ["15 cm", "15 km", "15 mm"]),
       ("걸어서 20분 걸리는 거리", "1 km", ["1 m", "1 cm", "100 km"]), ("개미의 몸 길이", "5 mm", ["5 cm", "5 m", "50 cm"]),
       ("한라산의 높이", "1950 m", ["1950 km", "1950 cm", "195 cm"]), ("손톱의 폭", "1 cm", ["1 m", "1 km", "10 m"]),
       ("마라톤 거리", "42 km", ["42 m", "42 cm", "420 m"]), ("연필의 길이", "17 cm", ["17 mm", "17 m", "170 cm"]),
       ("교실 문의 높이", "2 m", ["2 km", "2 cm", "2 mm"]), ("휴대 전화의 두께", "8 mm", ["8 cm", "8 m", "80 cm"])]


def estimate():
    t, a, w = R.choice(EST)
    return mcq("「%s」의 길이를 어림한 것으로 가장 알맞은 것은?" % t, a, w,
               "1 mm는 아주 짧고, 1 km는 걸어서 15분쯤 걸리는 거리예요. %s는 <b>%s</b>쯤이에요." % (t, a))


def calc():
    k = R.choice(["cm+", "cm-", "km+", "km-"])
    if k[:2] == "cm":
        a, b = R.randint(15, 99), R.randint(12, 80)
        if k == "cm-" and b >= a:
            return None
        if a % 10 == 0 or b % 10 == 0:
            return None
        r = a + b if k == "cm+" else a - b
        if r % 10 == 0 or r <= 0:
            return None
        op = "+" if k == "cm+" else "−"
        return mcq("%s %s %s =" % (cmmm(a), op, cmmm(b)), cmmm(r), [cmmm(r + 10), cmmm(r - 1) if r - 1 > 0 else cmmm(r + 2), cmmm(r + 1), "%d cm %d mm" % (r // 10, r % 10 + 10)],
                   "cm는 cm끼리, mm는 mm끼리 계산해요. mm끼리 10 mm가 넘거나 모자라면 1 cm = 10 mm로 바꾸어요. <b>%s</b>" % cmmm(r))
    a, b = R.randint(1200, 6800), R.randint(500, 3900)
    if a % 100 == 0 or b % 100 == 0 or (k == "km-" and b >= a):
        return None
    r = a + b if k == "km+" else a - b
    if r % 1000 == 0:
        return None
    op = "+" if k == "km+" else "−"
    return mcq("%s %s %s =" % (kmm(a), op, kmm(b)), kmm(r), [kmm(r + 1000), kmm(abs(r - 1000)) if r > 1000 else kmm(r + 100), kmm(r + 10), kmm(r - 100) if r > 100 else kmm(r + 200)],
               "km는 km끼리, m는 m끼리 계산해요. 1 km = 1000 m로 받아올림, 받아내림해요. <b>%s</b>" % kmm(r))


def story():
    who = NM.next()
    a, b = R.randint(1100, 3900), R.randint(600, 2900)
    if a % 100 == 0 or b % 100 == 0:
        return None
    k = R.choice(["add", "sub"])
    if k == "add":
        t = "%s 집에서 도서관까지 %s를 걸은 다음, 도서관에서 공원까지 %s를 더 걸었어요. 모두 몇 km 몇 m를 걸었나요?" % (josa(who, "은/는"), kmm(a), kmm(b))
        r = a + b
    else:
        if b >= a:
            return None
        t = "학교에서 기차역까지는 %s이고, 학교에서 우체국까지는 %s예요. 기차역이 우체국보다 몇 km 몇 m 더 먼가요?" % (kmm(a), kmm(b))
        r = a - b
    if r % 1000 == 0 or r < 1000:
        return None
    return mcq(t, kmm(r), [kmm(r + 1000), kmm(r - 100), kmm(r + 10), kmm(abs(a - b) if k == "add" else a + b)],
               "km는 km끼리, m는 m끼리 계산해요. <b>%s</b>" % kmm(r))


unit("grade-3", "length-mm-and-km", 6, "[4수03-15] [4수03-16]",
     "길이 단위 1mm와 1km를 알고, 이를 이용하여 길이를 측정하고 어림하며 수학의 유용성을 인식할 수 있다. 1cm와 1mm, 1km와 1m의 관계를 이해하고, 길이를 '몇 cm 몇 mm'와 '몇 mm', '몇 km 몇 m'와 '몇 m'로 다양하게 표현할 수 있다.",
     "1 mm와 1 km, 길이의 단위", "길이 (mm와 km)",
     "초등 3학년 길이 학습지: 자로 몇 cm 몇 mm 재기, cm와 mm, km와 m 바꾸기, 길이 어림하기, 길이의 덧셈과 뺄셈, 문장제까지 100문제와 정답.",
     "1 cm = 10 mm, 1 km = 1000 m", "같은 단위끼리 계산해요.",
     ["1 cm를 똑같이 10칸으로 나눈 작은 눈금 한 칸의 길이는 <b>1 mm</b>예요. 1 cm = 10 mm",
      "1000 m를 <b>1 km</b>라고 해요. 1 km = 1000 m",
      "자로 잴 때는 <b>눈금 0</b>에 물건의 끝을 맞추어요. 0이 아닌 곳에서 재기 시작하면 시작한 눈금만큼 빼요.",
      "길이를 더하고 뺄 때는 <b>cm는 cm끼리, mm는 mm끼리</b>(km는 km끼리, m는 m끼리) 계산해요."],
     [("4 cm 7 mm + 2 cm 8 mm =", ["mm끼리: 7 + 8 = 15 mm = 1 cm 5 mm", "cm끼리: 4 + 2 + 1 = 7 cm"], "7 cm 5 mm"),
      ("3 km 200 m − 1 km 500 m =", ["200 m에서 500 m를 뺄 수 없어요. 1 km = 1000 m를 받아내림해요.", "1200 − 500 = 700, 2 − 1 = 1"], "1 km 700 m")],
     [("1 km = 100 m라고 생각한다", "1 km는 1000 m예요."),
      ("자의 1 cm에서 재고 끝의 눈금을 그대로 읽는다", "시작한 눈금만큼 빼거나 0에 맞추어 재요."),
      ("mm끼리 더해서 10이 넘었는데 그대로 쓴다", "10 mm = 1 cm로 받아올림해요.")],
     [("1 mm와 1 km는 언제 배우나요?", "초등 3학년 1학기 「길이와 시간」 단원에서 배워요. cm와 m는 2학년에서 배웠어요."),
      ("1 km는 어느 정도인가요?", "어른 걸음으로 15분쯤, 운동장 200 m 트랙을 다섯 바퀴 도는 거리예요.")],
     [("자로 재기", [(measure, 20)]),
      ("cm와 mm", [(to_mm, 14), (compare_cm, 6)]),
      ("km와 m", [(to_m, 14), (compare_km, 6)]),
      ("길이 어림하기", [(estimate, 12), (measure, 8)]),
      ("길이의 덧셈과 뺄셈", [(calc, 12), (story, 8)])],
     82306)
