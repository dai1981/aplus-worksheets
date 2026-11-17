# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Time Zones and Duration (Australian Curriculum v9.0: AC9M8M04)
  python3 tools/gen_au_maths_y8_time_zones_and_duration.py
Converting between 12- and 24-hour time, finding durations (including past midnight), Australian time zones
(AWST, ACST, AEST and daylight saving), world times from UTC offsets, and travel problems.
Wrong answers come from real mistakes: adding 12 to a morning time, treating minutes as decimals (100 per hour),
going the wrong way between time zones, forgetting the half hour in South Australia and the Northern Territory,
and forgetting that Queensland does not use daylight saving.
"""
import random
from au_hs import B, S, make, lesson, collect, T, mcq

R = random.Random(81201)
DAY = 24 * 60


def t12(m):
    m %= DAY
    h, mi = divmod(m, 60)
    suf = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return "%d:%02d %s" % (h12, mi, suf)


def t24(m):
    m %= DAY
    return "%02d:%02d" % divmod(m, 60)


def dur(m):
    h, mi = divmod(m, 60)
    if h and mi:
        return "%d h %d min" % (h, mi)
    if h:
        return "%d hour%s" % (h, "" if h == 1 else "s")
    return "%d min" % mi


def TT(q, right, wrongs, e):
    ws = [w for w in dict.fromkeys(wrongs) if w != right]
    return T(q, right, ws[:3], e)


# ------------------------------------------------------------ set 1: 12- and 24-hour time
def one_conv(r):
    m = r.randint(0, DAY - 1) // 5 * 5
    if r.random() < 0.5:
        q = "Write %s in 24-hour time." % B(t12(m))
        h = m // 60
        wr = [t24(m + 12 * 60) if h < 12 else t24(m - 12 * 60), t24(m + 60), "%d:%02d" % (h % 12 or 12, m % 60)]
        e = ("Morning times keep their hour" if h < 12 else "For pm times add 12 to the hour") + (", but 12 am is 00:" if h == 0 else "") + ": <b>%s</b>." % t24(m)
        return TT(q, t24(m), wr, e)
    q = "Write %s in 12-hour time." % B(t24(m))
    wr = [t12(m + 12 * 60), t12(m - 120), t12(m + 120)]
    e = ("Hours 12 to 23 are pm; subtract 12 if the hour is more than 12" if m >= 720 else "Hours 00 to 11 are am") + ": <b>%s</b>." % t12(m)
    return TT(q, t12(m), wr, e)


# ------------------------------------------------------------ set 2: duration
def one_dur(r):
    a = r.randint(5 * 12, 22 * 12) * 5
    d = r.randint(3, 120) * 5
    if d < 30:
        return None
    b = a + d
    use24 = r.random() < 0.5
    f = t24 if use24 else t12
    q = "How long is it from %s to %s%s?" % (B(f(a)), B(f(b)), " the next morning" if b >= DAY and not use24 else (" the next day" if b >= DAY else ""))
    h, mi = divmod(d, 60)
    wrong_dec = (b // 60 * 100 + b % 60) - (a // 60 * 100 + a % 60)       # treating times like decimals
    w1 = dur(wrong_dec // 100 * 60 + wrong_dec % 100) if 0 < wrong_dec % 100 < 60 and wrong_dec > 0 else dur(d + 40)
    to_h = (60 - a % 60) % 60
    hrs, rest = divmod(d - to_h, 60)
    if to_h and d > to_h:
        more = ("%d h and %d min" % (hrs, rest)) if hrs and rest else ("%d h" % hrs if hrs else "%d min" % rest)
        e = "Count on: %s to %s is %d min, then %s more. Total <b>%s</b>." % (f(a), f(a + to_h), to_h, more, dur(d))
    else:
        e = "Count on from %s: %s. The time is <b>%s</b>." % (f(a), dur(d), dur(d))
    return TT(q, dur(d), [w1, dur(d + 60) if d > 60 else dur(d + 20), dur(abs(d - 60)) if d > 60 else dur(d + 10), dur(d + 12 * 60) if d < 12 * 60 else dur(d - 60)], e)


# ------------------------------------------------------------ set 3: Australian time zones
ZONES_STD = [("Perth", 8 * 60, "AWST"), ("Darwin", 9 * 60 + 30, "ACST"), ("Adelaide", 9 * 60 + 30, "ACST"),
             ("Brisbane", 10 * 60, "AEST"), ("Sydney", 10 * 60, "AEST"), ("Melbourne", 10 * 60, "AEST"),
             ("Hobart", 10 * 60, "AEST"), ("Canberra", 10 * 60, "AEST")]
DST = {"Adelaide", "Sydney", "Melbourne", "Hobart", "Canberra"}       # Perth, Darwin and Brisbane do not change


def off(city, summer):
    o = dict((c, x) for c, x, _ in ZONES_STD)[city]
    return o + (60 if summer and city in DST else 0)


def one_au(r):
    a, b = r.sample([c for c, _, _ in ZONES_STD], 2)
    summer = r.random() < 0.35
    oa, ob = off(a, summer), off(b, summer)
    if oa == ob:
        return None
    m = r.randint(6 * 12, 21 * 12) * 5
    ans = m + (ob - oa)
    month = "In January (daylight saving time)" if summer else "In June"
    q = "%s, it is %s in %s. What time is it in %s?" % (month, B(t12(m)), a, b)
    diff = ob - oa
    dtxt = ("%d h" % (abs(diff) // 60) if abs(diff) % 60 == 0 else ("%d h 30 min" % (abs(diff) // 60) if abs(diff) >= 60 else "30 min"))
    e = "%s is %s %s %s, so %s <b>%s</b>." % (b, dtxt, "ahead of" if diff > 0 else "behind", a, "add it:" if diff > 0 else "subtract it:", t12(ans))
    if summer and (a in DST) != (b in DST):
        e += " Only some states use daylight saving: Queensland, the Northern Territory and Western Australia do not."
    wr = [t12(m - diff), t12(m + diff + (30 if diff % 60 else 60)), t12(m + (off(b, not summer) - off(a, not summer))) if (off(b, not summer) - off(a, not summer)) != diff else t12(m + diff - 60)]
    return TT(q, t12(ans), wr + [t12(m + diff + 120)], e)


# ------------------------------------------------------------ set 4: world time zones (UTC offsets given)
WORLD = [("Sydney", 11), ("Perth", 8), ("Brisbane", 10), ("London", 0), ("Tokyo", 9), ("Singapore", 8),
         ("Auckland", 13), ("Los Angeles", -8), ("New York", -5), ("Dubai", 4), ("Jakarta", 7)]


def utc(o):
    return "UTC" + ("+%d" % o if o >= 0 else "−%d" % -o)


def one_world(r):
    (a, oa), (b, ob) = r.sample(WORLD, 2)
    if oa == ob:
        return None
    m = r.randint(0, DAY // 5 - 1) * 5
    diff = (ob - oa) * 60
    ans = m + diff
    day_note = ""
    if ans >= DAY:
        day_note = " the next day"
    elif ans < 0:
        day_note = " the day before"
    right = t12(ans) + day_note
    q = "In January, %s is %s and %s is %s. When it is %s on Monday in %s, what time is it in %s?" % (a, utc(oa), b, utc(ob), B(t12(m)), a, b)
    q = q.replace(" on Monday", "")
    k = abs(ob - oa)
    e = "%s is %d hour%s %s %s, so %s %d hour%s: <b>%s</b>." % (b, k, "" if k == 1 else "s", "ahead of" if diff > 0 else "behind", a,
                                                      "add" if diff > 0 else "subtract", k, "" if k == 1 else "s", right)
    def lab(t):
        return t12(t) + (" the next day" if t >= DAY else (" the day before" if t < 0 else ""))
    wr = [lab(m - diff), lab(m + diff + 60), lab(m + diff - 60), t12(ans)]
    return TT(q, right, [w for w in wr if w != right], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A flight leaves Perth at 9:00 am (AWST) and takes 4 hours to reach Sydney. In June, what is the local time in Sydney when it lands?", "3:00 pm",
         ["1:00 pm", "11:00 am", "5:00 pm"], "It lands at 1:00 pm Perth time. Sydney is 2 hours ahead in June: <b>3:00 pm</b>."),
        ("A flight leaves Sydney at 6:00 pm and takes 5 hours to reach Perth. In June, what is the local time in Perth when it lands?", "9:00 pm",
         ["11:00 pm", "1:00 am", "7:00 pm"], "It lands at 11:00 pm Sydney time. Perth is 2 hours behind: <b>9:00 pm</b>."),
        ("A cricket match in Adelaide starts at 1:30 pm (ACST, June). What time is this in Brisbane?", "2:00 pm", ["1:00 pm", "2:30 pm", "12:30 pm"], "Brisbane is 30 minutes ahead of Adelaide: <b>2:00 pm</b>."),
        ("In January, a TV show starts at 7:30 pm in Melbourne (AEDT). What time is it in Brisbane?", "6:30 pm", ["7:30 pm", "8:30 pm", "6:00 pm"],
         "Queensland does not use daylight saving, so in January Brisbane is 1 hour behind Melbourne: <b>6:30 pm</b>."),
        ("A bus leaves at 22:45 and arrives at 06:15 the next morning. How long is the trip?", "7 h 30 min", ["16 h 30 min", "8 h 30 min", "7 h 70 min"],
         "22:45 to 00:00 is 1 h 15 min. 00:00 to 06:15 is 6 h 15 min. Total <b>7 h 30 min</b>."),
        ("A train leaves Sydney at 07:42 and arrives in Canberra at 11:56. How long is the journey?", "4 h 14 min", ["4 h 54 min", "3 h 14 min", "4 h 4 min"], "07:42 to 11:42 is 4 h, then 14 min more: <b>4 h 14 min</b>."),
        ("In January (UTC+11), it is 8:00 pm in Sydney. London is UTC+0. What time is it in London?", "9:00 am", ["7:00 am", "9:00 pm", "11:00 am"],
         "London is 11 hours behind: 8:00 pm − 11 h = <b>9:00 am</b> the same day."),
        ("A flight from Sydney to Los Angeles leaves at 10:00 am on Friday and takes 14 hours. In January Sydney is UTC+11 and Los Angeles is UTC−8. What is the local time when it lands?", "5:00 am on Friday",
         ["12:00 am on Saturday", "5:00 am on Saturday", "7:00 pm on Friday"], "It lands at 12:00 am Saturday Sydney time. Los Angeles is 19 hours behind: <b>5:00 am on Friday</b>."),
        ("Which of these does NOT use daylight saving time?", "Queensland", ["New South Wales", "Victoria", "South Australia"],
         "<b>Queensland</b>, the Northern Territory and Western Australia stay on standard time all year."),
        ("How many hours ahead of Perth is Sydney in January (daylight saving)?", "3 hours", ["2 hours", "1 hour", "2.5 hours"], "In January Sydney is UTC+11 and Perth is UTC+8: <b>3 hours</b>."),
        ("A webinar starts at 4:00 pm in Brisbane. A student in Darwin (ACST) joins. What time is it in Darwin?", "3:30 pm", ["4:30 pm", "3:00 pm", "5:00 pm"], "Darwin is 30 minutes behind Brisbane all year: <b>3:30 pm</b>."),
        ("A shift starts at 21:30 and lasts 9 hours. When does it finish, in 24-hour time?", "06:30", ["30:30", "18:30", "05:30"], "21:30 + 9 h = 30:30, which is <b>06:30</b> the next day."),
        ("Ruby says 1.5 hours is 1 h 50 min. What is it really?", "1 h 30 min", ["1 h 50 min", "1 h 5 min", "150 min"], "0.5 of an hour is 30 minutes, so 1.5 h = <b>1 h 30 min</b>."),
        ("How many minutes are in 3¾ hours?", "225", ["375", "345", "180"], "3 × 60 + 45 = <b>225</b> minutes."),
        ("A runner finishes a marathon in 3 h 47 min. She started at 06:20. When does she finish?", "10:07", ["09:07", "10:47", "10:17"], "06:20 + 3 h = 09:20, + 47 min = <b>10:07</b>."),
        ("In June it is 12:00 pm in Melbourne. Where is it 10:00 am?", "Perth", ["Adelaide", "Brisbane", "Darwin"], "Perth is 2 hours behind Melbourne in June: <b>Perth</b>."),
        ("In January, Tokyo is UTC+9 and Adelaide is UTC+10:30. When it is 6:00 pm in Adelaide, what time is it in Tokyo?", "4:30 pm", ["7:30 pm", "5:00 pm", "4:00 pm"], "Tokyo is 1 h 30 min behind Adelaide: <b>4:30 pm</b>."),
        ("A ferry timetable shows departures every 35 minutes from 07:10. What is the time of the fourth departure?", "08:55", ["09:30", "08:20", "09:15"], "07:10, 07:45, 08:20, <b>08:55</b>."),
        ("How long is it from 11:40 pm Tuesday to 2:15 am Wednesday?", "2 h 35 min", ["9 h 25 min", "3 h 35 min", "2 h 25 min"], "11:40 pm to midnight is 20 min, then 2 h 15 min: <b>2 h 35 min</b>."),
        ("A phone call between Perth (UTC+8) and New York (UTC−5) is booked for 9:00 am Monday in New York. When is that in Perth?", "10:00 pm Monday",
         ["8:00 pm Sunday", "10:00 pm Sunday", "4:00 am Monday"], "Perth is 13 hours ahead: 9:00 am + 13 h = <b>10:00 pm Monday</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p><b>24-hour time</b> uses 00:00 to 23:59. For pm times add 12 to the hour (3:45 pm = 15:45); 12:30 am is 00:30.</p>"
        "<p>To find a <b>duration</b>, count on to the next hour, then whole hours, then the minutes. There are 60 minutes in an hour, not 100.</p>"
        "<p><b>Australian time zones</b>: Western Australia (AWST, UTC+8), South Australia and the Northern Territory (ACST, UTC+9:30), "
        "and the eastern states (AEST, UTC+10). In summer, New South Wales, Victoria, Tasmania, the ACT and South Australia move forward "
        "1 hour for daylight saving; Queensland, the Northern Territory and Western Australia do not.</p>"
        "<p>Going <b>east</b>, clocks are ahead, so add the difference. Going <b>west</b>, subtract it.</p>",
        [("How long is it from 9:50 am to 2:15 pm?", ["9:50 to 10:00 is 10 min.", "10:00 to 2:00 pm is 4 h.", "Then 15 min."], "4 h 25 min"),
         ("In June it is 4:00 pm in Sydney. What time is it in Perth?", ["Perth is 2 hours behind Sydney."], "2:00 pm"),
         ("In January it is 9:00 am in Brisbane. What time is it in Sydney?", ["Sydney is on daylight saving (UTC+11) but Brisbane is not (UTC+10)."], "10:00 am")],
        ["Treating time like decimals: 10:50 to 11:20 is 30 minutes, not 70.",
         "Adding 12 to a morning time when changing to 24-hour time.",
         "Going the wrong way: Perth is behind Sydney, so subtract.",
         "Forgetting the half hour for South Australia and the Northern Territory, or forgetting that Queensland has no daylight saving."])


def main():
    sets = [S("12-hour and 24-hour time", collect(one_conv, 20, R)),
            S("Finding durations", collect(one_dur, 20, R)),
            S("Australian time zones", collect(one_au, 20, R)),
            S("World time zones", collect(one_world, 20, R)),
            S("Time zone and travel problems", problems())]
    make(8, "time-zones-and-duration", 12, "AC9M8M04",
         "Time Zones and Duration: 12- and 24-Hour Time Across Australia and the World",
         "Year 8 Time Zones Worksheets: 24-Hour Time, Duration and Australian Time Zones (Free, Answer Key)",
         "Time zones and duration",
         "solve problems involving duration, including using 12- and 24-hour time across multiple time zones",
         "Free Year 8 maths worksheets on time for the Australian Curriculum (AC9M8M04): 12- and 24-hour time, durations past midnight, "
         "Australian time zones and daylight saving, world times from UTC offsets and flight problems. 100 questions with an answer key.",
         "Going east, clocks are ahead: add the time difference. Going west, subtract it.",
         "There are 60 minutes in an hour. Queensland, the NT and WA do not use daylight saving.",
         body(),
         [("What are Australia's time zones?", "AWST (UTC+8) in Western Australia, ACST (UTC+9:30) in South Australia and the Northern Territory, and AEST (UTC+10) in Queensland, New South Wales, the ACT, Victoria and Tasmania."),
          ("Which states use daylight saving?", "New South Wales, Victoria, Tasmania, the ACT and South Australia. Queensland, the Northern Territory and Western Australia do not."),
          ("How do I work out the time in another time zone?", "Find the difference between the two UTC offsets. Add it if the other place is further east (ahead), and subtract it if it is further west (behind)."),
          ("How do I find a duration that goes past midnight?", "Find the time to midnight, then add the time after midnight.")],
         sets, R)


if __name__ == "__main__":
    main()
