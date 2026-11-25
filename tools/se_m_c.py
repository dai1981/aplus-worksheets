# -*- coding: utf-8 -*-
"""Sverige åk 4–6: mätning och geometri（lv = 4, 5, 6）"""
import math
import random
from fractions import Fraction as F
import se_m as S
from se_m import num, kr, M, fr, fq, d, ri, ch, sh, cap, unit, tab
from se_common import wrap, text, line, fig, klocka, hm, INK, GREEN, FILL, RED, BLUE
from se_m_a import R0
import gen_au_maths_y5_angles as AU
import kr_pics56 as K56


def K():
    return S.K


# ============================================================ längd, massa och volym
LEN = {"mm": 1, "cm": 10, "dm": 100, "m": 1000, "km": 1000000, "mil": 10000000}
MAS = {"g": 1, "hg": 100, "kg": 1000, "ton": 1000000}
VOL = {"ml": 1, "cl": 10, "dl": 100, "l": 1000}


def enheter(lv):
    def omv(tab_, pairs, decimals):
        a, b = ch(pairs)
        f = F(tab_[a], tab_[b])
        if decimals and R0():
            x = F(ri(11, 99), 10) if f > 1 else F(ri(1, 99) * 10 ** ri(0, 1))
        else:
            x = F(ri(2, 9) if f > 1 else ri(2, 99) * (int(1 / f) if f < 1 else 1))
        try:
            v = d(x * f)
            xs = d(x)
        except ValueError:
            return None
        w = [x * f * 10, x * f / 10, x * f * 100 if f >= 1 else x * f / 100]
        try:
            ws = [d(z) + " " + b for z in w]
        except ValueError:
            return None
        return M("%s %s = ? %s" % (xs, a, b), v + " " + b, ws, "1 %s = %s %s. %s %s = <b>%s %s</b>." % (a, d(f), b, xs, a, v, b))

    lpairs = [("m", "cm"), ("dm", "cm"), ("cm", "mm"), ("km", "m"), ("mil", "km"), ("m", "mm"), ("cm", "m"), ("mm", "cm"), ("m", "km")]
    mpairs = [("kg", "g"), ("kg", "hg"), ("hg", "g"), ("g", "kg")] + ([("ton", "kg"), ("kg", "ton")] if lv >= 5 else [])
    vpairs = [("l", "dl"), ("l", "ml"), ("dl", "cl"), ("dl", "ml"), ("cl", "ml"), ("dl", "l"), ("ml", "l")]

    def langd():
        return omv(LEN, lpairs[:6] if lv == 4 else lpairs, lv >= 5)

    def massa():
        return omv(MAS, mpairs[:3] if lv == 4 else mpairs, lv >= 5)

    def volym():
        if lv == 6 and R0():
            k = ri(0, 1)
            if k == 0:
                n = ri(2, 30)
                return M("%d dm³ = ? liter" % n, "%d l" % n, ["%d l" % (n * 10), "%s l" % num(n * 1000), "%s l" % d(F(n, 10))], "1 dm³ = 1 liter. %d dm³ = <b>%d l</b>." % (n, n))
            n = ri(2, 900)
            return M("%d cm³ = ? ml" % n, "%d ml" % n, ["%s ml" % num(n * 10), "%s ml" % num(n * 1000), "%s ml" % d(F(n, 10))], "1 cm³ = 1 ml. %d cm³ = <b>%d ml</b>." % (n, n))
        return omv(VOL, vpairs[:5] if lv == 4 else vpairs, lv >= 5)

    def jamfor():
        tab_, us = ch([(LEN, ["mm", "cm", "dm", "m"]), (MAS, ["g", "hg", "kg"]), (VOL, ["ml", "cl", "dl", "l"])])
        xs = []
        for _ in range(4):
            u_ = ch(us)
            xs.append((ri(1, 30) * (10 if u_ in ("mm", "g", "ml") else 1), u_))
        vals = [v * tab_[u_] for v, u_ in xs]
        if len(set(vals)) < 4:
            return None
        big = R0()
        k = vals.index(max(vals) if big else min(vals))
        f_ = lambda t: "%d %s" % t
        return M("Vilket är %s? %s" % ("störst" if big else "minst", ", ".join(f_(t) for t in xs)), f_(xs[k]), [f_(t) for i, t in enumerate(xs) if i != k],
                 "Gör om till samma enhet: %s. %s är %s." % (", ".join("%s = %s %s" % (f_(t), num(v), us[0]) for t, v in zip(xs, vals)), f_(xs[k]), "störst" if big else "minst"))

    def uppsk():
        opts = [("Hur lång är en vuxen människa ungefär?", "1,7 m", ["17 m", "17 cm", "1,7 km"]), ("Hur mycket väger en liter mjölk ungefär?", "1 kg", ["1 g", "10 kg", "1 hg"]),
                ("Hur mycket rymmer en tekopp ungefär?", "2 dl", ["2 l", "20 ml", "20 l"]), ("Hur lång är en skolbuss ungefär?", "12 m", ["12 dm", "120 m", "1,2 km"]),
                ("Hur mycket väger en personbil ungefär?", "1,5 ton", ["15 kg", "150 kg", "15 ton"]), ("Hur lång är en blyertspenna ungefär?", "18 cm", ["18 mm", "18 dm", "1,8 m"]),
                ("Hur mycket rymmer en badbalja för en bebis ungefär?", "20 l", ["20 dl", "200 l", "2 l"]), ("Hur mycket väger ett äpple ungefär?", "150 g", ["15 g", "1,5 kg", "15 kg"]),
                ("Hur långt är det från Stockholm till Göteborg ungefär?", "47 mil", ["47 km", "4,7 mil", "470 mil"]), ("Hur tjock är en mobiltelefon ungefär?", "8 mm", ["8 cm", "8 dm", "0,8 mm"]),
                ("Hur mycket väger en hund av mellanstorlek ungefär?", "20 kg", ["20 hg", "200 kg", "2 kg"]), ("Hur mycket rymmer en vattenflaska ungefär?", "50 cl", ["50 ml", "50 l", "5 ml"])]
        q, a, w = ch(opts)
        return M(q, a, w, "Ett rimligt värde är <b>%s</b>." % a)

    def text_():
        n = K().name()
        k = ri(0, 3)
        if k == 0:
            a, b = ri(1, 4), ri(20, 90)
            c = ri(50, 95)
            return M("%s har ett rep som är %d m %d cm. %s klipper av %d cm. Hur långt är repet nu?" % (n, a, b, n, c), "%d cm" % (100 * a + b - c),
                     ["%d cm" % x for x in (a * 100 + b + c, a + b - c if a + b > c else 100 * a + b - c + 10, 10 * a + b - c if 10 * a + b > c else 100 * a - c)], "%d m %d cm = %d cm. %d − %d = <b>%d cm</b>." % (a, b, 100 * a + b, 100 * a + b, c, 100 * a + b - c))
        if k == 1:
            l, g = ri(1, 3), ch([2, 25, 5]) if lv >= 5 else ch([2, 5])
            gl = ch([2, 25]) if False else 2
            return M("En kanna rymmer %d l saft. Hur många glas på %d dl kan du hälla upp?" % (l, gl), str(10 * l // gl), [str(l * gl), str(10 * l), str(10 * l // gl + 1)],
                     "%d l = %d dl. %d : %d = <b>%d glas</b>." % (l, 10 * l, 10 * l, gl, 10 * l // gl))
        if k == 2:
            a, b = ri(3, 9), ri(2, 8)
            return M("En väska väger %d kg och %d hg. %s lägger i en bok som väger %d hg. Hur mycket väger väskan nu?" % (a, b, n, 10 - b), "%d kg" % (a + 1),
                     ["%d kg %d hg" % (a, 10), "%d kg" % a, "%d hg" % (a + 10)], "%d hg + %d hg = 10 hg = 1 kg. Väskan väger <b>%d kg</b>." % (b, 10 - b, a + 1))
        km = ri(12, 95)
        return M("Från %s hem till mormor är det %d km. Hur många mil är det?" % (n, km) if False else "Det är %d km till mormors stuga. Hur många mil är det?" % km, "%s mil" % d(F(km, 10)),
                 ["%d mil" % km, "%s mil" % d(F(km, 100)), "%s mil" % num(km * 10)], "10 km = 1 mil. %d km = <b>%s mil</b>." % (km, d(F(km, 10))))

    sets = [("Längd", [(langd, 20)]), ("Massa", [(massa, 20)]), ("Volym", [(volym, 20)]), ("Jämför och uppskatta", [(jamfor, 10), (uppsk, 10)]), ("Textuppgifter", [(text_, 20)])]
    return unit("langd-massa-och-volym", "G", "Längd, massa och volym: enheter och omvandling", "Längd, massa och volym",
                "Jämförelse, uppskattning och mätning av längd, massa och volym med vanliga måttenheter. Omvandling mellan enheter%s." % (" och tal i decimalform" if lv >= 5 else ""),
                "Arbetsblad om enheter för årskurs %d: längd (mm, cm, dm, m, km, mil), massa (g, hg, kg%s) och volym (ml, cl, dl, l%s), jämför, uppskatta och textuppgifter. 100 uppgifter med facit." % (lv, ", ton" if lv >= 5 else "", ", dm³, cm³" if lv == 6 else ""),
                "Gör om till samma enhet", "1 m = 100 cm, 1 kg = 1 000 g, 1 l = 10 dl", sets,
                ["Längd: 1 cm = 10 mm, 1 dm = 10 cm, 1 m = 100 cm, 1 km = 1 000 m och 1 mil = 10 km.",
                 "Massa: 1 kg = 10 hg = 1 000 g" + (" och 1 ton = 1 000 kg" if lv >= 5 else "") + ". Volym: 1 l = 10 dl = 100 cl = 1 000 ml" + (", 1 dm³ = 1 l och 1 cm³ = 1 ml." if lv == 6 else "."),
                 "Till en mindre enhet multiplicerar du och till en större enhet dividerar du. Jämför bara när enheterna är lika."],
                [("3,5 m = ? cm", ["1 m = 100 cm", "3,5 · 100"], "350 cm"), ("Vilket är mest, 750 g eller 1 kg?", ["1 kg = 1 000 g"], "1 kg")],
                [["3,5 m = 35 cm", "1 m = 100 cm: 350 cm"], ["800 g är mer än 1 kg eftersom 800 &gt; 1", "Gör om: 1 kg = 1 000 g"],
                 ["1 mil = 1 000 m", "1 mil = 10 km = 10 000 m"]],
                [("Vad är skillnaden mellan massa och vikt?", "I vardagen säger vi vikt. I matematiken mäts massa i gram och kilogram."),
                 ("Hur mycket är ett hekto?", "Ett hektogram är 100 gram."),
                 ("Varför finns mil?", "Mil är en gammal svensk enhet för långa avstånd. En mil är 10 kilometer.")])


# ============================================================ tid
def tid(lv):
    def f_(m):
        h, mm = divmod(m, 60)
        if h == 0:
            return "%d minuter" % mm
        return ("%d timme" % h if h == 1 else "%d timmar" % h) + (" %d minuter" % mm if mm else "")

    def digital():
        h, m = ri(13, 23), ch(range(0, 60, 5))
        k = ri(0, 1)
        h12 = h - 12
        part = "på eftermiddagen" if h < 18 else "på kvällen"
        if k == 0:
            return M("Klockan är %s. Vad visar en 12-timmarsklocka?" % hm(h, m), "%s %s" % (hm(h12, m), part), ["%s %s" % (hm(h12, m), "på förmiddagen"), "%s %s" % (hm(h - 10, m), part), "%s %s" % (hm(h12 + 1, m), part)],
                     "%d − 12 = %d. <b>%s %s</b>." % (h, h12, hm(h12, m), part))
        return M("Klockan är %s %s. Hur skrivs det med 24 timmar?" % (hm(h12, m), part), hm(h, m), [hm(h12, m), hm(h + 1 if h < 23 else h - 1, m), hm(h, (m + 30) % 60)],
                 "Efter klockan 12 lägger du till 12: %d + 12 = <b>%s</b>." % (h12, hm(h, m)))

    def skillnad():
        h1, m1 = ri(7, 17), ch(range(0, 60, 5))
        dd = ri(20, 230 if lv == 5 else 150) // 5 * 5
        t = h1 * 60 + m1 + dd
        if t >= 24 * 60:
            return None
        act = ch(["Tåget avgår", "Matchen börjar", "Filmen börjar", "Simträningen börjar", "Bussen avgår"])
        tail = {"Tåget avgår": "kommer fram", "Bussen avgår": "kommer fram"}.get(act, "slutar")
        return M("%s %s och %s %s. Hur lång tid tar det?" % (act, hm(h1, m1), tail, hm(t // 60, t % 60)), f_(dd),
                 [f_(x) for x in (dd + 40 if (t % 60) < m1 else dd + 10, dd - 10, dd + 60) if x > 0],
                 "Räkna till nästa hel timme och sedan vidare: <b>%s</b>." % f_(dd))

    def senare():
        h, m = ri(6, 20), ch(range(0, 60, 5))
        dd = ri(25, 175) // 5 * 5
        t = h * 60 + m + dd
        if t >= 24 * 60:
            return None
        g = hm(t // 60, t % 60)
        early = R0()
        if early:
            t2 = h * 60 + m - dd
            if t2 < 0:
                return None
            g2 = hm(t2 // 60, t2 % 60)
            return M("Klockan är %s. Vad var klockan för %s sedan?" % (hm(h, m), f_(dd)), g2, [hm(t2 // 60 + 1, t2 % 60), hm(t2 // 60, (t2 % 60 + 10) % 60), g],
                     "%s − %s = <b>%s</b>." % (hm(h, m), f_(dd), g2))
        return M("Klockan är %s. Vad är klockan om %s?" % (hm(h, m), f_(dd)), g, [hm(t // 60 + 1, t % 60) if t // 60 < 23 else hm(t // 60 - 1, t % 60), hm(t // 60, (t % 60 + 10) % 60), hm(h + dd // 60, (m + dd) % 60) if hm(h + dd // 60, (m + dd) % 60) != g else hm(t // 60, (t % 60 + 20) % 60)],
                 "%s + %s = <b>%s</b>." % (hm(h, m), f_(dd), g))

    def enheter():
        k = ri(0, 6)
        if k == 0:
            n = ri(2, 6)
            return M("Hur många minuter är %d timmar?" % n, str(60 * n), [str(100 * n), str(60 + n), str(24 * n)], "1 timme = 60 minuter. %d · 60 = <b>%d</b>." % (n, 60 * n))
        if k == 1:
            n = ri(2, 9)
            return M("Hur många sekunder är %d minuter?" % n, str(60 * n), [str(100 * n), str(n * 10), str(60 + n)], "1 minut = 60 sekunder. %d · 60 = <b>%d</b>." % (n, 60 * n))
        if k == 2:
            n = ri(2, 7)
            return M("Hur många timmar är %d dygn?" % n, str(24 * n), [str(12 * n), str(60 * n), str(24 + n)], "1 dygn = 24 timmar. %d · 24 = <b>%d</b>." % (n, 24 * n))
        if k == 3:
            n = ri(70, 200)
            return M("Hur många timmar och minuter är %d minuter?" % n, f_(n), [f_(n + 40), "%d timmar %d minuter" % (n // 100, n % 100) if n % 100 < 60 and n // 100 > 1 else f_(n - 10), f_(n + 10)],
                     "60 minuter är 1 timme. %d minuter = <b>%s</b>." % (n, f_(n)))
        if k == 4:
            w = ri(2, 10)
            return M("Hur många dagar är %d veckor?" % w, str(7 * w), [str(5 * w), str(7 + w), str(10 * w)], "1 vecka = 7 dagar. %d · 7 = <b>%d</b>." % (w, 7 * w))
        if k == 5:
            q = ch([("Hur många dagar har ett vanligt år?", "365", ["360", "366", "352"]), ("Hur många dagar har ett skottår?", "366", ["365", "364", "360"]),
                    ("Hur många månader har ett år?", "12", ["10", "52", "4"]), ("Hur många veckor har ett år ungefär?", "52", ["12", "48", "100"])])
            return M(q[0], q[1], q[2], "Svar: <b>%s</b>." % q[1])
        y = ri(2010, 2019)
        n = ri(5, 12)
        return M("%s föddes år %d. Hur gammal fyller %s år %d?" % (K().name(), y, "hen", y + n) if False else "En skola byggdes år %d. Hur många år har det gått år %d?" % (y - 50, y + n), "%d år" % (50 + n),
                 ["%d år" % x for x in (n, 50 + n + 1, 50 - n)], "%d − %d = <b>%d år</b>." % (y + n, y - 50, 50 + n))

    def tidtabell():
        st = ["Centrum", "Skolan", "Badhuset", "Torget", "Stationen"]
        h = ri(7, 16)
        m0 = ri(0, 5) * 5
        gaps = [ri(3, 12) for _ in range(4)]
        times = [h * 60 + m0]
        for g in gaps:
            times.append(times[-1] + g)
        rows = [[s, hm(t // 60, t % 60)] for s, t in zip(st, times)]
        a, b = sorted(sh(range(5))[:2])
        dd = times[b] - times[a]
        return M(tab(["Hållplats", "Avgång"], rows) + "Hur lång tid tar bussen från %s till %s?" % (st[a], st[b]), "%d minuter" % dd,
                 ["%d minuter" % x for x in (dd + 5, dd - 2 if dd > 2 else dd + 2, times[b] % 60 - times[a] % 60 + 60 if times[b] % 60 < times[a] % 60 else dd + 10)],
                 "%s − %s = <b>%d minuter</b>." % (hm(times[b] // 60, times[b] % 60), hm(times[a] // 60, times[a] % 60), dd))

    sets = [("12 och 24 timmar", [(digital, 20)]), ("Vad är klockan sedan?", [(senare, 20)]), ("Hur lång tid?", [(skillnad, 20)]),
            ("Tidtabeller", [(tidtabell, 20)]), ("Tidsenheter", [(enheter, 20)])]
    return unit("tid", "G", "Tid: 24-timmarsklockan, tidsskillnad och tidtabeller", "Tid",
                "Jämförelse, uppskattning och mätning av tid med vanliga måttenheter. 12- och 24-timmarsklocka, tidsskillnader och tidtabeller.",
                "Arbetsblad om tid för årskurs %d: 12- och 24-timmarsklockan, vad klockan är sedan, hur lång tid något tar, tidtabeller och tidsenheter. 100 uppgifter med facit." % lv,
                "Hoppa till nästa hela timme", "En timme har 60 minuter, inte 100.", sets,
                ["24-timmarsklockan räknar vidare efter 12: klockan 3 på eftermiddagen är 15.00 och halv åtta på kvällen är 19.30.",
                 "För att räkna ut hur lång tid något tar hoppar du först till nästa hela timme och räknar sedan vidare. Från 9.45 till 11.20: 15 minuter + 1 timme + 20 minuter.",
                 "1 minut = 60 sekunder, 1 timme = 60 minuter, 1 dygn = 24 timmar och 1 vecka = 7 dagar."],
                [("Från 9.45 till 11.20", ["9.45 → 10.00: 15 min", "10.00 → 11.00: 1 timme", "11.00 → 11.20: 20 min"], "1 timme 35 minuter"),
                 ("Klockan är 14.50. Vad är klockan om 25 minuter?", ["14.50 + 10 min = 15.00", "15.00 + 15 min"], "15.15")],
                [["9.45 till 11.20 = 1 timme 75 minuter", "En timme har 60 minuter: 1 timme 35 minuter"], ["15.30 = halv fyra på förmiddagen", "15.30 är på eftermiddagen"],
                 ["14.50 + 25 minuter = 14.75", "Det finns ingen 14.75: 15.15"]],
                [("Varför står det 17.45 på tågbiljetten?", "Tidtabeller använder 24-timmarsklockan så att man inte blandar ihop förmiddag och eftermiddag."),
                 ("Hur skriver man klockslag?", "Med punkt mellan timmar och minuter: 8.05 eller 18.30."),
                 ("Vad är ett dygn?", "24 timmar, från midnatt till midnatt.")])


# ============================================================ omkrets och area
def rect_svg(w, h, labels=True, unit_="cm", grid=False):
    k = min(26, 200 // max(w, h))
    s = []
    if grid:
        for i in range(w + 1):
            s.append(line(20 + i * k, 14, 20 + i * k, 14 + h * k, "#9bb", 1))
        for j in range(h + 1):
            s.append(line(20, 14 + j * k, 20 + w * k, 14 + j * k, "#9bb", 1))
    s.append("<rect x='20' y='14' width='%d' height='%d' fill='%s' fill-opacity='%s' stroke='%s' stroke-width='2.5'/>" % (w * k, h * k, FILL, "0.5" if grid else "1", GREEN))
    if labels:
        s.append(text(20 + w * k / 2.0, 14 + h * k + 20, "%d %s" % (w, unit_), 13))
        s.append(text(20 + w * k + 8, 14 + h * k / 2.0 + 5, "%d %s" % (h, unit_), 13, anchor="start"))
    return wrap(w * k + 80, h * k + 44, "".join(s), "rektangel %d gånger %d" % (w, h))


def lshape(a, b, c, dd):
    """L-form: hel bredd a, hel höjd b, urskuren c × dd uppe till höger"""
    k = min(18, 220 // max(a, b))
    pts = [(0, 0), (a - c, 0), (a - c, dd), (a, dd), (a, b), (0, b)]
    P = " ".join("%d,%d" % (60 + x * k, 22 + y * k) for x, y in pts)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (P, FILL, GREEN)]
    s.append(text(60 + a * k / 2.0, 22 + b * k + 20, "%d cm" % a, 13))
    s.append(text(60 - 8, 22 + b * k / 2.0 + 5, "%d cm" % b, 13, anchor="end"))
    s.append(text(60 + (a - c) * k / 2.0, 22 - 6, "%d cm" % (a - c), 13))
    s.append(text(60 + a * k + 8, 22 + (dd + b) * k / 2.0 + 5, "%d cm" % (b - dd), 13, anchor="start"))
    return wrap(a * k + 130, b * k + 52, "".join(s), "sammansatt figur")


def tri_svg(b, h):
    k = min(22, 220 // max(b, h))
    off = ri(0, b)
    pts = [(20, 14 + h * k), (20 + b * k, 14 + h * k), (20 + off * k, 14)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%d,%d" % p for p in pts), FILL, GREEN)]
    s.append(line(20 + off * k, 14, 20 + off * k, 14 + h * k, RED, 1.6, " stroke-dasharray='5 3'"))
    s.append(text(20 + b * k / 2.0, 14 + h * k + 20, "%d cm" % b, 13))
    s.append(text(20 + off * k + 6, 14 + h * k / 2.0 + 5, "%d cm" % h, 13, anchor="start", col=RED))
    return wrap(b * k + 80, h * k + 44, "".join(s), "triangel med höjd")


def omkrets_area(lv):
    def rutor():
        w, h = ri(2, 8), ri(2, 6)
        if w == h:
            return None
        if R0():
            return M(rect_svg(w, h, False, grid=True) + "Hur många rutor täcker rektangeln? Varje ruta är 1 cm².", "%d cm²" % (w * h), ["%d cm²" % x for x in (2 * (w + h), w + h, w * h + w)],
                     "%d rader med %d rutor: %d · %d = <b>%d cm²</b>." % (h, w, h, w, w * h))
        return M(rect_svg(w, h, False, grid=True) + "Hur lång är omkretsen? Varje ruta är 1 cm lång.", "%d cm" % (2 * (w + h)), ["%d cm" % x for x in (w * h, w + h, 2 * w + h)] if w * h != 2 * (w + h) else ["%d cm" % x for x in (w + h, 2 * w + h, 2 * (w + h) + 2)],
                 "Räkna alla sidor: %d + %d + %d + %d = <b>%d cm</b>." % (w, h, w, h, 2 * (w + h)))

    def rekt():
        w, h = ri(3, 15), ri(2, 12)
        if w == h:
            return None
        if R0():
            return M(rect_svg(w, h) + "Vad är rektangelns area?", "%d cm²" % (w * h), ["%d cm²" % x for x in (2 * (w + h), w + h, w * h + h)] + ["%d cm" % (w * h)],
                     "Area = längd · bredd = %d · %d = <b>%d cm²</b>." % (w, h, w * h))
        return M(rect_svg(w, h) + "Vad är rektangelns omkrets?", "%d cm" % (2 * (w + h)), ["%d cm" % x for x in (w * h, w + h, 2 * w + h)] + ["%d cm²" % (2 * (w + h))],
                 "Omkrets = %d + %d + %d + %d = <b>%d cm</b>." % (w, h, w, h, 2 * (w + h)))

    def baklanges():
        w, h = ri(3, 12), ri(2, 9)
        if R0():
            return M("En rektangel har arean %d cm² och längden %d cm. Hur bred är den?" % (w * h, w), "%d cm" % h, ["%d cm" % x for x in (w * h - w, h + 1, w * h // 2)],
                     "Area = längd · bredd. %d : %d = <b>%d cm</b>." % (w * h, w, h))
        return M("En kvadrat har omkretsen %d cm. Hur lång är en sida?" % (4 * w), "%d cm" % w, ["%d cm" % x for x in (2 * w, 4 * w // 2 + 1, w * w)] if w != 4 else ["%d cm" % x for x in (8, 3, 5)],
                 "En kvadrat har 4 lika långa sidor: %d : 4 = <b>%d cm</b>." % (4 * w, w))

    def triangel():
        b, h = ri(3, 14), ri(2, 10)
        if b * h % 2:
            return None
        return M(tri_svg(b, h) + "Vad är triangelns area?", "%d cm²" % (b * h // 2), ["%d cm²" % x for x in (b * h, b + h, b * h // 2 + b)],
                 "Area = bas · höjd : 2 = %d · %d : 2 = <b>%d cm²</b>." % (b, h, b * h // 2))

    def sammansatt():
        a, b = ri(6, 12), ri(5, 10)
        c, dd = ri(2, a - 3), ri(2, b - 3)
        area = a * b - c * dd
        if R0():
            return M(lshape(a, b, c, dd) + "Vad är figurens area?", "%d cm²" % area, ["%d cm²" % x for x in (a * b, a * b + c * dd, 2 * (a + b))],
                     "Hela rektangeln %d · %d = %d minus hörnet %d · %d = %d: <b>%d cm²</b>." % (a, b, a * b, c, dd, c * dd, area))
        return M(lshape(a, b, c, dd) + "Vad är figurens omkrets?", "%d cm" % (2 * (a + b)), ["%d cm" % x for x in (2 * (a + b) - c - dd, area, a + b + c + dd)],
                 "Hacket flyttar bara sidorna. Omkretsen blir lika lång som för en rektangel %d · %d: <b>%d cm</b>." % (a, b, 2 * (a + b)))

    def enheter():
        k = ri(0, 2)
        if k == 0:
            n = ri(2, 9)
            return M("%d m² = ? dm²" % n, "%d dm²" % (100 * n), ["%d dm²" % (10 * n), "%s dm²" % num(1000 * n), "%d dm²" % n], "1 m² = 10 dm · 10 dm = 100 dm². %d m² = <b>%d dm²</b>." % (n, 100 * n))
        if k == 1:
            n = ri(2, 9)
            return M("%d dm² = ? cm²" % n, "%d cm²" % (100 * n), ["%d cm²" % (10 * n), "%s cm²" % num(1000 * n), "%d cm²" % n], "1 dm² = 10 cm · 10 cm = 100 cm². %d dm² = <b>%d cm²</b>." % (n, 100 * n))
        w, h = ri(3, 12), ri(3, 9)
        return M("Ett rum är %d m långt och %d m brett. Hur stor är golvytan?" % (w, h), "%d m²" % (w * h), ["%d m²" % x for x in (2 * (w + h), w + h)] + ["%d m" % (w * h)],
                 "%d · %d = <b>%d m²</b>." % (w, h, w * h))

    def parallellogram():
        b, h = ri(3, 12), ri(2, 9)
        s = []
        k = 16
        sl = ri(1, 3)
        pts = [(20 + sl * k, 14), (20 + (b + sl) * k, 14), (20 + b * k, 14 + h * k), (20, 14 + h * k)]
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join("%d,%d" % p for p in pts), FILL, GREEN))
        s.append(line(20 + (b + sl) * k - 4, 14, 20 + (b + sl) * k - 4, 14 + h * k, RED, 1.6, " stroke-dasharray='5 3'"))
        s.append(text(20 + b * k / 2.0, 14 + h * k + 20, "%d cm" % b, 13))
        s.append(text(20 + (b + sl) * k + 2, 14 + h * k / 2.0 + 5, "%d cm" % h, 13, anchor="start", col=RED))
        pic = wrap((b + sl) * k + 80, h * k + 44, "".join(s), "parallellogram med höjd")
        return M(pic + "Vad är parallellogrammets area?", "%d cm²" % (b * h), ["%d cm²" % x for x in (b * h // 2 if b * h % 2 == 0 else b * h + 1, 2 * (b + h), b + h)],
                 "Area = bas · höjd = %d · %d = <b>%d cm²</b>." % (b, h, b * h))

    if lv == 4:
        sets = [("Räkna rutor", [(rutor, 20)]), ("Rektangelns area", [(rekt, 20)]), ("Omkrets och area", [(rekt, 10), (rutor, 10)]),
                ("Räkna baklänges", [(baklanges, 20)]), ("Area i vardagen", [(enheter, 20)])]
    elif lv == 5:
        sets = [("Rektangelns omkrets och area", [(rekt, 20)]), ("Triangelns area", [(triangel, 20)]), ("Räkna baklänges", [(baklanges, 20)]),
                ("Sammansatta figurer", [(sammansatt, 20)]), ("Areaenheter", [(enheter, 20)])]
    else:
        sets = [("Rektangel och kvadrat", [(rekt, 10), (baklanges, 10)]), ("Triangelns area", [(triangel, 20)]), ("Parallellogrammets area", [(parallellogram, 20)]),
                ("Sammansatta figurer", [(sammansatt, 20)]), ("Areaenheter", [(enheter, 20)])]
    return unit("omkrets-och-area", "G", "Omkrets och area" + (": rektangel, triangel och sammansatta figurer" if lv >= 5 else " för rektanglar"), "Omkrets och area",
                "Metoder för hur omkrets och area hos olika tvådimensionella geometriska figurer kan bestämmas och uppskattas. Mätning av area med vanliga måttenheter.",
                "Arbetsblad om omkrets och area för årskurs %d: %s. 100 uppgifter med facit." % (lv, "räkna rutor, rektangelns omkrets och area och areaenheter" if lv == 4 else
                                                                                             "rektangel, triangel, sammansatta figurer och areaenheter" if lv == 5 else "rektangel, triangel, parallellogram, sammansatta figurer och areaenheter"),
                "Omkrets runt om, area inuti", "Area mäts i cm² och m².", sets,
                ["Omkrets är längden runt en figur. Lägg ihop alla sidor: en rektangel som är 6 cm och 4 cm har omkretsen 6 + 4 + 6 + 4 = 20 cm.",
                 "Area är hur stor yta figuren täcker. En rektangel har arean längd · bredd: 6 · 4 = 24 cm²." + (" En triangel har arean bas · höjd : 2." if lv >= 5 else ""),
                 "Area mäts i kvadratcentimeter (cm²) och kvadratmeter (m²). 1 m² = 100 dm² och 1 dm² = 100 cm²."],
                [("Rektangel 7 cm och 3 cm", ["Omkrets: 7 + 3 + 7 + 3 = 20 cm", "Area: 7 · 3 = 21 cm²"], "20 cm och 21 cm²"),
                 ("Triangel med bas 8 cm och höjd 5 cm", ["8 · 5 = 40", "40 : 2"], "20 cm²") if lv >= 5 else ("Arean 24 cm², längden 6 cm", ["24 : 6"], "bredden 4 cm")],
                [["Blandar ihop omkrets och area", "Omkrets är runt om (cm), area är ytan (cm²)"], ["Omkrets = 7 + 3 = 10 cm", "Alla fyra sidor: 20 cm"],
                 ["Triangelns area = bas · höjd", "Dela med 2"] if lv >= 5 else ["Skriver arean i cm", "Arean skrivs i cm²"]],
                [("Vad betyder cm²?", "Kvadratcentimeter: en kvadrat som är 1 cm lång och 1 cm bred."),
                 ("Kan två figurer ha samma area men olika omkrets?", "Ja. En rektangel 12 · 2 och en 6 · 4 har båda arean 24 cm², men olika omkrets."),
                 ("Varför är 1 m² = 100 dm²?", "En kvadrat med sidan 1 m = 10 dm rymmer 10 · 10 = 100 kvadrater med sidan 1 dm.")])


# ============================================================ vinklar
def vinklar(lv):
    def typ_(v):
        return "rät vinkel" if v == 90 else "spetsig vinkel" if v < 90 else "trubbig vinkel" if v < 180 else "rak vinkel"

    def klass():
        v = ch([ri(15, 80), 90, ri(100, 170)] + ([180] if lv >= 5 else []))
        pic = fig(AU.angle_fig(v, ri(0, 40), "vinkel").replace("marked angle", "vinkel"))
        return M(pic + "Vilken sorts vinkel är det?", typ_(v), [x for x in ("spetsig vinkel", "rät vinkel", "trubbig vinkel", "rak vinkel") if x != typ_(v)],
                 "%s. Den är <b>%s</b>." % ("Mindre än en rät vinkel" if v < 90 else "Precis 90°" if v == 90 else "Större än en rät vinkel" if v < 180 else "180°, en rak linje", typ_(v)))

    def grader():
        v = ri(10, 175)
        if v == 90:
            return None
        return M("En vinkel är %d°. Vilken sorts vinkel är det?" % v, typ_(v), [x for x in ("spetsig vinkel", "rät vinkel", "trubbig vinkel", "rak vinkel") if x != typ_(v)],
                 "Spetsig: mindre än 90°. Trubbig: mellan 90° och 180°. %d° är en <b>%s</b>." % (v, typ_(v)))

    def gradskiva():
        v = ri(3, 34) * 5
        if v == 90:
            return None
        pic = fig(AU.protractor_svg([0, v], "gradskiva").replace("<svg ", "<svg data-pf='lg' ", 1))
        return M(pic + "Hur stor är vinkeln som de röda strålarna bildar?", "%d°" % v, ["%d°" % (180 - v), "%d°" % (v + 10), "%d°" % (v - 5 if lv >= 5 else v - 10)],
                 "Läs på den skala som börjar på 0 där den ena strålen ligger: <b>%d°</b>." % v)

    def uppsk():
        v = ch([30, 45, 60, 120, 135, 150, 20, 160])
        pic = fig(AU.angle_fig(v, ri(0, 60), "vinkel"))
        w = [x for x in (30, 45, 60, 90, 120, 135, 150, 170) if abs(x - v) >= 30][:6]
        R_ = S.R
        R_.shuffle(w)
        return M(pic + "Ungefär hur stor är vinkeln?", "%d°" % v, ["%d°" % x for x in w], "Jämför med en rät vinkel (90°). Vinkeln är ungefär <b>%d°</b>." % v)

    def summa():
        a, b = ri(25, 90), ri(25, 90)
        c = 180 - a - b
        if c < 15:
            return None
        pic = fig(AU.shape_svg(AU.tri_pts(a, b), {0: "%d°" % a, 1: "%d°" % b, 2: "?"}, "triangel", rights=[i for i, x in enumerate((a, b, c)) if x == 90 and i != 2]))
        return M(pic + "Hur stor är vinkeln med frågetecknet?", "%d°" % c, ["%d°" % x for x in (360 - a - b, a + b, 90 - c if c < 90 else c - 10, c + 10)],
                 "Vinkelsumman i en triangel är 180°. 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))

    def rak():
        a = ri(20, 160)
        if a == 90:
            return None
        if R0():
            return M("Två vinklar bildar tillsammans en rak vinkel. Den ena är %d°. Hur stor är den andra?" % a, "%d°" % (180 - a), ["%d°" % x for x in (360 - a, 90 - a if a < 90 else a - 90, a)],
                     "En rak vinkel är 180°. 180° − %d° = <b>%d°</b>." % (a, 180 - a))
        b, c = ri(70, 120), ri(50, 110)
        e = 360 - a - b - c
        if not 30 <= e <= 170:
            return None
        return M("En fyrhörning har vinklarna %d°, %d° och %d°. Hur stor är den fjärde vinkeln?" % (a, b, c), "%d°" % e, ["%d°" % x for x in (180 - (a + b + c) % 180, e + 10, 360 - e)],
                 "Vinkelsumman i en fyrhörning är 360°. 360° − %d° − %d° − %d° = <b>%d°</b>." % (a, b, c, e))

    if lv == 4:
        sets = [("Spetsig, rät eller trubbig", [(klass, 20)]), ("Vinklar i grader", [(grader, 20)]), ("Uppskatta vinklar", [(uppsk, 20)]),
                ("Mäta med gradskiva", [(gradskiva, 20)]), ("Blandat", [(klass, 7), (grader, 7), (uppsk, 6)])]
    elif lv == 5:
        sets = [("Vinkeltyper", [(klass, 10), (grader, 10)]), ("Uppskatta vinklar", [(uppsk, 20)]), ("Mäta med gradskiva", [(gradskiva, 20)]),
                ("Rak vinkel", [(rak, 20)]), ("Blandat", [(klass, 10), (rak, 10)])]
    else:
        sets = [("Vinkeltyper", [(klass, 10), (grader, 10)]), ("Mäta med gradskiva", [(gradskiva, 20)]), ("Raka vinklar och fyrhörningar", [(rak, 20)]),
                ("Vinkelsumman i en triangel", [(summa, 20)]), ("Blandat", [(summa, 10), (rak, 10)])]
    return unit("vinklar", "G", "Vinklar: vinkeltyper, gradskiva och vinkelsummor" if lv == 6 else "Vinklar: vinkeltyper och gradskiva", "Vinklar",
                "Jämförelse, uppskattning och mätning av vinklar med vanliga måttenheter. Grundläggande geometriska objekt och deras egenskaper.",
                "Arbetsblad om vinklar för årskurs %d: spetsig, rät och trubbig vinkel, vinklar i grader, uppskatta, mäta med gradskiva%s. 100 uppgifter med facit." % (lv, ", rak vinkel och vinkelsumman i en triangel" if lv == 6 else ", rak vinkel" if lv == 5 else ""),
                "En rät vinkel är 90°", "Spetsig: under 90°. Trubbig: mellan 90° och 180°.", sets,
                ["Vinklar mäts i grader (°). En rät vinkel är 90°, som hörnet på ett papper. En rak vinkel är 180°.",
                 "En spetsig vinkel är mindre än 90° och en trubbig vinkel är mellan 90° och 180°.",
                 "När du mäter med gradskiva lägger du mittpunkten på vinkelns spets och 0-linjen längs ena strålen. Läs på den skala som börjar på 0."
                 + (" Vinkelsumman i en triangel är 180° och i en fyrhörning 360°." if lv == 6 else "")],
                [("En vinkel är 125°", ["Större än 90°", "Mindre än 180°"], "trubbig vinkel"), ("Triangel med 50° och 70°", ["180 − 50 − 70"], "60°") if lv == 6 else ("Vinkel och 35° bildar en rak vinkel", ["180 − 35"], "145°")],
                [["Läser på fel skala på gradskivan", "Börja på den skala som visar 0 vid ena strålen"], ["Tror att långa strålar ger en större vinkel", "Vinkelns storlek beror bara på öppningen"],
                 ["Vinkelsumman i en triangel är 360°", "Den är 180°"] if lv == 6 else ["Kallar 90° för en trubbig vinkel", "90° är en rät vinkel"]],
                [("Vad betyder grader här?", "Ett mått på hur stor öppningen är mellan två strålar. Ett helt varv är 360°."),
                 ("Hur ser jag om en vinkel är rät?", "Lägg ett pappershörn i vinkeln. Passar det precis är vinkeln rät."),
                 ("Spelar det roll hur långa strålarna är?", "Nej, bara hur mycket de öppnar sig.")])


# ============================================================ geometriska figurer och kroppar
FYR = [("kvadrat", "fyra lika långa sidor och fyra räta vinklar"), ("rektangel", "fyra räta vinklar och motstående sidor lika långa"),
       ("romb", "fyra lika långa sidor men inga räta vinklar"), ("parallellogram", "två par parallella sidor men inga räta vinklar"),
       ("parallelltrapets", "bara ett par parallella sidor")]
KROPP = {"kub": (6, 12, 8), "rätblock": (6, 12, 8), "pyramid med kvadratisk bas": (5, 8, 5), "tresidigt prisma": (5, 9, 6), "tetraeder": (4, 6, 4)}


def figurer(lv):
    def polygon():
        n = ri(3, 8)
        nm = {3: "triangel", 4: "fyrhörning", 5: "femhörning", 6: "sexhörning", 7: "sjuhörning", 8: "åttahörning"}[n]
        pts = ["%.1f,%.1f" % (60 + 44 * math.cos(math.radians(-90 + i * 360.0 / n + ri(-8, 8))), 56 + 44 * math.sin(math.radians(-90 + i * 360.0 / n + ri(-8, 8)))) for i in range(n)]
        pic = wrap(120, 112, "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>" % (" ".join(pts), FILL, GREEN), "en månghörning")
        others = [v for k, v in {3: "triangel", 4: "fyrhörning", 5: "femhörning", 6: "sexhörning", 7: "sjuhörning", 8: "åttahörning"}.items() if k != n]
        return M(pic + "Vad heter månghörningen?", nm, sh(others), "Räkna hörnen: %d hörn ger en <b>%s</b>." % (n, nm))

    def fyrhorning():
        nm, desc = ch(FYR)
        return M("Vilken fyrhörning har %s?" % desc, nm, [x for x, _ in sh(FYR) if x != nm], "Det är en <b>%s</b>." % nm)

    def sant():
        opts = [("Alla kvadrater är rektanglar.", "sant"), ("Alla rektanglar är kvadrater.", "falskt"), ("En romb har fyra lika långa sidor.", "sant"),
                ("En triangel kan ha två räta vinklar.", "falskt"), ("En parallellogram har två par parallella sidor.", "sant"), ("En cirkel är en månghörning.", "falskt"),
                ("En kvadrat är en romb.", "sant"), ("En liksidig triangel har tre lika långa sidor.", "sant"), ("En parallelltrapets har fyra räta vinklar.", "falskt"),
                ("Diagonalerna i en rektangel är lika långa.", "sant"), ("En sexhörning har fem sidor.", "falskt"), ("En rektangel har fyra symmetrilinjer.", "falskt")]
        q, a = ch(opts)
        return M("Sant eller falskt? <i>%s</i>" % q, a, ["falskt" if a == "sant" else "sant", "bara ibland", "det går inte att veta"], "Påståendet är <b>%s</b>." % a)

    def kropp():
        nm = ch(list(KROPP))
        f, e, v = KROPP[nm]
        what = ch(["sidoytor", "kanter", "hörn"])
        n = {"sidoytor": f, "kanter": e, "hörn": v}[what]
        art = "ett" if nm in ("rätblock", "tresidigt prisma") else "en"
        c = ri(2, 5)
        if R0():
            pl = {"kub": "kuber", "rätblock": "rätblock", "pyramid med kvadratisk bas": "pyramider med kvadratisk bas", "tresidigt prisma": "tresidiga prismor", "tetraeder": "tetraedrar"}[nm]
            return M("Hur många %s har %d %s tillsammans?" % (what, c, pl), str(c * n), [str(c * n + c), str(c + n), str(c * n - n), str(n)],
                     "%s %s har %d %s. %d · %d = <b>%d</b>." % (cap(art), nm, n, what, c, n, c * n))
        return M("Hur många %s har %s %s?" % (what, art, nm), str(n), [str(x) for x in sh({f, e, v, n + 1, n - 1, n + 2} - {n})],
                 "%s %s har %d sidoytor, %d kanter och %d hörn." % (cap(art), nm, f, e, v))

    def kropp_namn():
        opts = [("Vilken kropp har två cirklar som basytor och en buktig sida?", "cylinder", ["kon", "klot", "prisma"]),
                ("Vilken kropp har en cirkel som bas och en spets?", "kon", ["cylinder", "pyramid", "klot"]),
                ("Vilken kropp har sex kvadratiska sidoytor?", "kub", ["rätblock", "prisma", "pyramid"]),
                ("Vilken kropp har en månghörning som bas och trianglar som sidoytor som möts i en spets?", "pyramid", ["prisma", "kon", "kub"]),
                ("Vilken kropp har två likadana trianglar som basytor och rektanglar som sidor?", "tresidigt prisma", ["pyramid", "rätblock", "kon"]),
                ("Vilken kropp har inga kanter och inga hörn?", "klot", ["cylinder", "kon", "kub"]),
                ("Vilken kropp liknar ett mjölkpaket?", "rätblock", ["kub", "cylinder", "prisma"]), ("Vilken kropp liknar en konservburk?", "cylinder", ["kon", "rätblock", "klot"]),
                ("Vilken kropp liknar en glasstrut?", "kon", ["pyramid", "cylinder", "klot"]), ("Vilken kropp liknar en Toblerone-förpackning?", "tresidigt prisma", ["pyramid", "rätblock", "cylinder"])]
        q, a, w = ch(opts[:-1])
        return M(q, a, w, "Rätt svar: <b>%s</b>." % a)

    def natet():
        opts = [("Vilken kropp kan du vika av ett nät med sex kvadrater?", "kub"), ("Vilken kropp får du av ett nät med en kvadrat och fyra trianglar?", "pyramid med kvadratisk bas"),
                ("Vilken kropp får du av ett nät med två cirklar och en rektangel?", "cylinder"), ("Vilken kropp får du av ett nät med två trianglar och tre rektanglar?", "tresidigt prisma"),
                ("Vilken kropp får du av ett nät med sex rektanglar?", "rätblock"), ("Vilken kropp får du av ett nät med fyra liksidiga trianglar?", "tetraeder")]
        q, a = ch(opts)
        return M(q, a, [x for x in ("kub", "rätblock", "cylinder", "tresidigt prisma", "pyramid med kvadratisk bas", "tetraeder") if x != a][:3] if False else sh([x for x in ("kub", "rätblock", "cylinder", "tresidigt prisma", "pyramid med kvadratisk bas", "tetraeder") if x != a]),
                 "Vik ihop nätet i tanken. Det blir <b>%s</b>." % a)

    def volym():
        l, b, h = ri(2, 10), ri(2, 8), ri(2, 6)
        v = l * b * h
        k = ri(0, 2)
        if k == 0:
            return M("Ett rätblock är %d cm långt, %d cm brett och %d cm högt. Vad är volymen?" % (l, b, h), "%d cm³" % v, ["%d cm³" % x for x in (l + b + h, l * b, 2 * (l * b + l * h + b * h))],
                     "Volym = längd · bredd · höjd = %d · %d · %d = <b>%d cm³</b>." % (l, b, h, v))
        if k == 1:
            return M("En låda är %d dm lång, %d dm bred och %d dm hög. Hur många liter rymmer den?" % (l, b, h), "%s liter" % num(v), ["%s liter" % num(x) for x in (l * b, v * 10, l + b + h)],
                     "%d · %d · %d = %d dm³ = <b>%d liter</b>." % (l, b, h, v, v))
        return M("Ett rätblock har volymen %d cm³. Bottenytan är %d cm · %d cm. Hur högt är det?" % (v, l, b), "%d cm" % h, ["%d cm" % x for x in (v // l, h + 1, v - l * b)],
                 "%d · %d = %d. %d : %d = <b>%d cm</b>." % (l, b, l * b, v, l * b, h))

    def kuber():
        a, b, c = ri(2, 5), ri(2, 4), ri(1, 4)
        cells = [(x, y, z) for x in range(a) for y in range(b) for z in range(c)]
        pic = K56.iso_cubes(cells, label="rätblock av kuber", A=20, front=False)
        return M(pic + "Rätblocket är byggt av små kuber. Hur många kuber är det?", str(a * b * c), [str(a + b + c), str(a * b), str(a * b * c + a)],
                 "%d · %d i varje lager och %d lager: %d · %d · %d = <b>%d</b>." % (a, b, c, a, b, c, a * b * c))

    if lv == 4:
        sets = [("Månghörningar", [(polygon, 20)]), ("Fyrhörningar", [(fyrhorning, 5), (sant, 10), (polygon, 5)]), ("Kroppar", [(kropp_namn, 9), (kropp, 11)]),
                ("Sidoytor, kanter och hörn", [(kropp, 20)]), ("Nät och kuber", [(natet, 6), (kuber, 14)])]
    elif lv == 5:
        sets = [("Månghörningar", [(polygon, 20)]), ("Fyrhörningar", [(fyrhorning, 5), (sant, 10), (polygon, 5)]), ("Kroppar och nät", [(kropp_namn, 9), (natet, 6), (kropp, 5)]),
                ("Sidoytor, kanter och hörn", [(kropp, 10), (kuber, 10)]), ("Bygga med kuber", [(kuber, 20)])]
    else:
        sets = [("Fyrhörningar", [(fyrhorning, 5), (sant, 10), (polygon, 5)]), ("Kroppar och nät", [(kropp_namn, 9), (natet, 6), (kropp, 5)]), ("Bygga med kuber", [(kuber, 20)]),
                ("Volym av rätblock", [(volym, 20)]), ("Blandat", [(polygon, 10), (kropp, 10)])]
    return unit("geometriska-figurer-och-kroppar", "G", "Geometriska figurer och kroppar" + (" och volym" if lv == 6 else ""), "Figurer och kroppar",
                "Grundläggande geometriska objekt, däribland polygoner, cirklar, klot, koner, cylindrar och rätblock samt deras inbördes relationer och egenskaper.",
                "Arbetsblad om geometriska figurer och kroppar för årskurs %d: månghörningar, fyrhörningar, kroppar, sidoytor, kanter och hörn, nät%s. 100 uppgifter med facit." % (lv, " och volym" if lv == 6 else " och bygga med kuber"),
                "Räkna hörn, kanter och ytor", "En kub har 6 sidoytor, 12 kanter och 8 hörn.", sets,
                ["En månghörning (polygon) är en sluten figur med raka sidor. Den får namn efter antalet hörn: triangel, fyrhörning, femhörning och så vidare.",
                 "Fyrhörningar: en kvadrat har fyra lika långa sidor och räta vinklar, en rektangel har räta vinklar, en romb har fyra lika långa sidor och en parallellogram har två par parallella sidor.",
                 "En kropp har sidoytor, kanter och hörn. Ett rätblock har 6 sidoytor, 12 kanter och 8 hörn." + (" Volymen av ett rätblock är längd · bredd · höjd." if lv == 6 else "")],
                [("Kanter på ett tresidigt prisma", ["3 kanter upptill, 3 nertill, 3 på sidorna"], "9"), ("Rätblock 5 cm, 3 cm, 2 cm", ["5 · 3 · 2"], "30 cm³") if lv == 6 else ("Är en kvadrat en rektangel?", ["Den har fyra räta vinklar"], "ja")],
                [["En kvadrat är inte en rektangel", "Den har fyra räta vinklar, alltså är den en rektangel"], ["Räknar bara kanterna som syns", "Räkna även de dolda: 12 på ett rätblock"],
                 ["Volym = längd + bredd + höjd", "Multiplicera: längd · bredd · höjd"] if lv == 6 else ["Blandar ihop sidoyta och kant", "En kant är där två ytor möts"]],
                [("Vad är skillnaden mellan figur och kropp?", "En figur är platt (två dimensioner). En kropp har längd, bredd och höjd."),
                 ("Vad är ett prisma?", "En kropp med två likadana basytor och rektanglar mellan dem."),
                 ("Vad är ett nät?", "En utvikt kropp. Viker du ihop nätet får du kroppen.")])


# ============================================================ symmetri och spegling
import gen_de_mathe_k3_achsensymmetrie as SY


def symmetri(lv):
    SY.R = random.Random(S.R.random())

    def _sv(s):
        return s.replace("vier Figuren A bis D", "fyra figurer A till D").replace("halbe Figur mit Spiegelachse", "halv figur med symmetrilinje")

    def vilken():
        hs = [SY.half() for _ in range(4)]
        if not all(hs):
            return None
        good = SY.mirror(hs[0])
        bads = [SY.broken(SY.mirror(hs[1])), SY.shifted(hs[2]), SY.broken(SY.mirror(hs[3]))]
        if not all(bads) or any(b == SY.mirror({(x, y) for x, y in b if x < 3}) for b in bads):
            return None
        figs = bads + [good]
        SY.R.shuffle(figs)
        k = figs.index(good)
        return M(_sv(SY.four(figs)) + "Vilken figur är symmetrisk kring den röda linjen?", "ABCD"[k], ["ABCD"[i] for i in range(4) if i != k],
                 "Bara i figur %s ligger rutorna på båda sidor lika långt från linjen." % "ABCD"[k])

    def fyll():
        h = SY.half()
        if not h:
            return None
        good = SY.mirror(h)
        near = SY.broken(good)
        opts = [good, SY.shifted(h), near, set(h) | {(SY.COLS - 1 - x, SY.ROWS - 1 - y) for x, y in h}]
        if not near or len({frozenset(o) for o in opts}) < 4:
            return None
        pic = _sv(wrap(SY.COLS * SY.Q + 20, SY.ROWS * SY.Q + 20, SY.grid(10, 10, h), "halv figur med symmetrilinje"))
        SY.R.shuffle(opts)
        k = opts.index(good)
        return M(pic + "Spegla figuren i den röda linjen. Vilken bild visar resultatet?" + _sv(SY.four(opts)), "ABCD"[k], ["ABCD"[i] for i in range(4) if i != k],
                 "Varje ruta speglas lika långt på andra sidan linjen. Rätt är <b>%s</b>." % "ABCD"[k])

    LINJER = [("en kvadrat", "4"), ("en rektangel som inte är en kvadrat", "2"), ("en liksidig triangel", "3"), ("en cirkel", "oändligt många"),
              ("en likbent triangel", "1"), ("en romb som inte är en kvadrat", "2"), ("en regelbunden sexhörning", "6"), ("en regelbunden femhörning", "5"),
              ("en parallellogram som inte är en rektangel", "ingen"), ("bokstaven H", "2"), ("bokstaven E", "1"), ("bokstaven N", "ingen"), ("siffran 8", "2")]

    def linjer():
        t, a = ch(LINJER)
        near = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "oändligt många": ["1", "4"], "1": ["2", "ingen"], "6": ["3", "12"], "5": ["10", "1"], "ingen": ["1", "2"]}[a]
        return M("Hur många symmetrilinjer har %s?" % t, a, near + sh([x for x in ("ingen", "1", "2", "3", "4", "6", "oändligt många") if x != a]),
                 "%s har <b>%s</b> symmetrilinje%s." % (cap(t), a, "" if a in ("1", "ingen") else "r"))

    def punkt():
        x, y = ri(1, 9), ri(1, 9)
        ax = ri(2, 8)
        if x == ax:
            return None
        mx = 2 * ax - x
        if not 0 <= mx <= 12:
            return None
        return M("Punkten (%d, %d) speglas i den lodräta linjen x = %d. Vilka koordinater får spegelpunkten?" % (x, y, ax), "(%d, %d)" % (mx, y),
                 ["(%d, %d)" % (x, 2 * ax - y) if 0 <= 2 * ax - y else "(%d, %d)" % (y, x), "(%d, %d)" % (ax, y), "(%d, %d)" % (mx + 1, y), "(%d, %d)" % (y, mx)],
                 "Punkten ligger %d steg %s om linjen. Spegelpunkten ligger lika långt på andra sidan: <b>(%d, %d)</b>." % (abs(x - ax), "till vänster" if x < ax else "till höger", mx, y))

    sets = [("Är figuren symmetrisk?", [(vilken, 20)]), ("Spegla figuren", [(fyll, 20)]), ("Antal symmetrilinjer", [(linjer, 13), (vilken, 7)]),
            ("Spegling i koordinatsystem", [(punkt, 20)]), ("Blandat", [(fyll, 10), (punkt, 10)])]
    return unit("symmetri", "G", "Symmetri och spegling", "Symmetri",
                "Symmetri, till exempel i bilder och i naturen, och hur symmetri kan konstrueras. Spegling i en linje.",
                "Arbetsblad om symmetri för årskurs %d: symmetriska figurer, spegla en figur, antal symmetrilinjer och spegling i ett koordinatsystem. 100 uppgifter med facit." % lv,
                "Lika långt på andra sidan", "Spegelbilden har samma avstånd till linjen.", sets,
                ["En figur är symmetrisk om den kan vikas längs en linje så att halvorna passar precis. Linjen heter symmetrilinje.",
                 "Vid spegling hamnar varje punkt lika långt från linjen fast på andra sidan. Det som ligger nära linjen hamnar nära linjen.",
                 "En figur kan ha flera symmetrilinjer: en kvadrat har 4, en liksidig triangel 3 och en cirkel oändligt många."],
                [("(2, 5) speglas i linjen x = 4", ["2 ligger 2 steg till vänster om 4", "2 steg till höger: 6"], "(6, 5)"), ("Symmetrilinjer i en rektangel", ["En lodrät och en vågrät"], "2")],
                [["Flyttar figuren i stället för att spegla den", "Spegla: närmast linjen förblir närmast linjen"], ["Diagonalen i en rektangel är en symmetrilinje", "Viker du längs diagonalen passar inte halvorna"],
                 ["Ändrar y-koordinaten vid spegling i en lodrät linje", "Bara x ändras"]],
                [("Var finns symmetri?", "I naturen (fjärilar, blad), i flaggor, bokstäver och byggnader."),
                 ("Hur testar jag symmetri?", "Vik papperet längs linjen, eller håll en spegel på linjen."),
                 ("Vad är en spegelbild?", "Bilden av figuren på andra sidan symmetrilinjen.")])


# ============================================================ koordinatsystem
from de_k8 import kosy


def koordinat(lv):
    hi = 10 if lv <= 5 else 10

    def las():
        x, y = ri(1, hi - 1), ri(1, hi - 1)
        if x == y:
            return None
        pic = fig(kosy(pts=[(x, y, "A")], lo=0, hi=hi, u=22, label="koordinatsystem").replace("<svg ", "<svg data-pf='lg' ", 1).replace("Koordinatensystem", "koordinatsystem"))
        return M(pic + "Vilka koordinater har punkten A?", "(%d, %d)" % (x, y), ["(%d, %d)" % (y, x), "(%d, %d)" % (x + 1, y), "(%d, %d)" % (x, y - 1)],
                 "Gå först %d steg åt höger (x) och sedan %d steg uppåt (y): <b>(%d, %d)</b>." % (x, y, x, y))

    def vilken():
        pts = []
        while len(pts) < 4:
            p = (ri(1, hi - 1), ri(1, hi - 1))
            if p not in pts:
                pts.append(p)
        names = "ABCD"
        pic = fig(kosy(pts=[(x, y, n) for (x, y), n in zip(pts, names)], lo=0, hi=hi, u=22, label="koordinatsystem").replace("<svg ", "<svg data-pf='lg' ", 1).replace("Koordinatensystem", "koordinatsystem"))
        k = ri(0, 3)
        x, y = pts[k]
        return M(pic + "Vilken punkt har koordinaterna (%d, %d)?" % (x, y), names[k], [names[i] for i in range(4) if i != k],
                 "x = %d åt höger och y = %d uppåt: punkt <b>%s</b>." % (x, y, names[k]))

    def ordning():
        x, y = ri(1, 9), ri(1, 9)
        if x == y:
            return None
        return M("Vad betyder den första siffran i punkten (%d, %d)?" % (x, y), "%d steg åt höger längs x-axeln" % x,
                 ["%d steg uppåt längs y-axeln" % x, "%d steg åt höger längs x-axeln" % y, "punktens nummer"], "Den första koordinaten är x: <b>%d steg åt höger</b>." % x)

    def flytta():
        x, y = ri(1, 8), ri(1, 8)
        dx, dy = ri(-3, 3), ri(-3, 3)
        if dx == 0 or dy == 0 or not (0 <= x + dx <= 10 and 0 <= y + dy <= 10):
            return None
        hx = "%d steg %s" % (abs(dx), "åt höger" if dx > 0 else "åt vänster")
        hy = "%d steg %s" % (abs(dy), "uppåt" if dy > 0 else "nedåt")
        return M("Punkten (%d, %d) flyttas %s och %s. Var hamnar den?" % (x, y, hx, hy), "(%d, %d)" % (x + dx, y + dy),
                 ["(%d, %d)" % p for p in ((x + dy, y + dx), (x - dx, y + dy), (x + dx, y - dy), (x + dx + 1, y + dy), (y + dy, x + dx)) if min(p) >= 0], "x: %d %s %d = %d, y: %d %s %d = %d. Svar: <b>(%d, %d)</b>." % (
                     x, "+" if dx > 0 else "−", abs(dx), x + dx, y, "+" if dy > 0 else "−", abs(dy), y + dy, x + dx, y + dy))

    def fjarde():
        x, y = ri(1, 5), ri(1, 5)
        w, h = ri(2, 4), ri(2, 4)
        pts = [(x, y), (x + w, y), (x + w, y + h)]
        return M("Tre hörn i en rektangel är (%d, %d), (%d, %d) och (%d, %d). Vilka koordinater har det fjärde hörnet?" % (pts[0] + pts[1] + pts[2]), "(%d, %d)" % (x, y + h),
                 ["(%d, %d)" % (x + w, y + h + 1), "(%d, %d)" % (y + h, x), "(%d, %d)" % (x + h, y + w) if (x + h, y + w) != (x, y + h) else "(%d, %d)" % (x + 1, y + h)],
                 "Det fjärde hörnet har samma x som (%d, %d) och samma y som (%d, %d): <b>(%d, %d)</b>." % (x, y, x + w, y + h, x, y + h))

    def gradering():
        st = ch([2, 5, 10, 20, 50])
        k = ri(1, 9)
        v = k * st
        return M("På y-axeln står talen 0, %d, %d, %d … med lika stora steg. Vilket tal står vid det %d:e strecket efter 0?" % (st, 2 * st, 3 * st, k), num(v),
                 [num(k), num(v + st), num(v - st) if v > st else num(v * 2)], "Varje steg är %d. %d · %d = <b>%s</b>." % (st, k, st, num(v)))

    if lv == 4:
        sets = [("Läs av punkter", [(las, 20)]), ("Hitta punkten", [(vilken, 20)]), ("x först, sedan y", [(ordning, 6), (las, 14)]),
                ("Flytta punkter", [(flytta, 20)]), ("Rektanglar i koordinatsystemet", [(fjarde, 20)])]
    else:
        sets = [("Läs av punkter", [(las, 20)]), ("Hitta punkten", [(vilken, 20)]), ("Flytta punkter", [(flytta, 20)]),
                ("Rektanglar i koordinatsystemet", [(fjarde, 20)]), ("Gradera axlar", [(gradering, 20)])]
    return unit("koordinatsystem", "F", "Koordinatsystem: läsa av och placera punkter", "Koordinatsystem",
                "Koordinatsystem och strategier för gradering av koordinataxlar. Läsa av och placera punkter.",
                "Arbetsblad om koordinatsystem för årskurs %d: läs av punkter, hitta punkten, flytta punkter, rektanglar i koordinatsystemet%s. 100 uppgifter med facit." % (lv, " och gradera axlar" if lv >= 5 else ""),
                "Först x, sedan y", "(3, 5) betyder 3 åt höger och 5 uppåt.", sets,
                ["Ett koordinatsystem har en vågrät x-axel och en lodrät y-axel som möts i origo (0, 0).",
                 "En punkt skrivs (x, y). Gå först längs x-axeln åt höger och sedan uppåt längs y-axeln. (3, 5) och (5, 3) är olika punkter.",
                 "Axlarna kan graderas med olika steg, till exempel 2, 5 eller 10. Läs vad varje streck är värt innan du läser av."],
                [("Var ligger (4, 2)?", ["4 steg åt höger", "2 steg uppåt"], "i punkten (4, 2)"), ("(3, 6) flyttas 2 åt höger", ["x: 3 + 2 = 5", "y är kvar"], "(5, 6)")],
                [["Byter plats på x och y", "x först: (åt höger, uppåt)"], ["Räknar rutor i stället för linjer", "Punkterna ligger där linjerna korsar varandra"],
                 ["Tror att varje streck alltid är 1", "Kontrollera hur axeln är graderad"]],
                [("Vad är origo?", "Punkten (0, 0), där axlarna möts."),
                 ("Varför är ordningen viktig?", "(2, 7) och (7, 2) är olika platser. Kom ihåg: först åt sidan, sedan uppåt."),
                 ("Var används koordinater?", "I kartor, i spel som sänka skepp och när man programmerar figurer på en skärm.")])


# ============================================================ skala
def skala(lv):
    def karta():
        s_ = ch([10000, 20000, 25000, 50000, 100000])
        cm = ri(2, 12)
        real_cm = cm * s_
        m = real_cm // 100
        ans = "%s m" % num(m) if m < 1000 or m % 1000 else "%s km" % num(m // 1000)
        if m >= 1000 and m % 1000 == 0:
            ans = "%s km" % num(m // 1000)
        elif m >= 1000:
            ans = "%s km" % d(F(m, 1000))
        w = ["%s m" % num(m // 10), "%s km" % num(cm * s_ // 1000) if cm * s_ // 1000 else "%d m" % cm, "%s m" % num(m * 10)]
        return M("En karta har skalan 1 : %s. Avståndet på kartan är %d cm. Hur långt är det i verkligheten?" % (num(s_), cm), ans, w,
                 "%d cm · %s = %s cm = <b>%s</b>." % (cm, num(s_), num(real_cm), ans))

    def ritning():
        s_ = ch([10, 20, 50, 100])
        cm = ri(2, 15)
        real = cm * s_
        return M("En ritning har skalan 1 : %d. En vägg är %d cm på ritningen. Hur lång är väggen i verkligheten?" % (s_, cm), "%s m" % d(F(real, 100)),
                 ["%s m" % d(F(real, 10)), "%d m" % cm, "%s m" % d(F(real, 1000))], "%d cm · %d = %s cm = <b>%s m</b>." % (cm, s_, num(real), d(F(real, 100))))

    def forstoring():
        s_ = ch([2, 3, 4, 5, 10])
        mm = ri(2, 12)
        if R0():
            return M("En bild av en insekt är ritad i skalan %d : 1. Insekten är %d mm i verkligheten. Hur lång är den på bilden?" % (s_, mm), "%d mm" % (mm * s_),
                     ["%d mm" % x for x in (mm + s_, mm, mm * s_ + mm)], "Skalan %d : 1 betyder %d gånger större: %d · %d = <b>%d mm</b>." % (s_, s_, mm, s_, mm * s_))
        return M("En bild är ritad i skalan %d : 1. På bilden är ett frö %d mm. Hur stort är fröet i verkligheten?" % (s_, mm * s_), "%d mm" % mm,
                 ["%d mm" % x for x in (mm * s_ * s_, mm * s_ - s_, mm + s_)], "Dela med %d: %d : %d = <b>%d mm</b>." % (s_, mm * s_, s_, mm))

    def vilken():
        a = ri(2, 9)
        k = ch([2, 3, 4, 10])
        big = R0()
        if big:
            return M("En figur med sidan %d cm ritas så att sidan blir %d cm. Vilken skala är det?" % (a, a * k), "%d : 1" % k, ["1 : %d" % k, "%d : %d" % (a, a * k), "%d : 1" % (a * k)],
                     "Bilden är %d gånger större: skalan är <b>%d : 1</b>." % (k, k))
        return M("En figur med sidan %d cm ritas så att sidan blir %d cm. Vilken skala är det?" % (a * k, a), "1 : %d" % k, ["%d : 1" % k, "1 : %d" % (a * k), "%d : %d" % (a, k)],
                 "Bilden är %d gånger mindre: skalan är <b>1 : %d</b>." % (k, k))

    def baklanges():
        s_ = ch([10000, 20000, 25000, 50000, 100000])
        km = ri(1, 9) * {20000: 1, 25000: 1}.get(s_, 1)
        cm = km * 100000 // s_
        return M("Två byar ligger %d km från varandra. Hur långt är det på en karta med skalan 1 : %s?" % (km, num(s_)), "%d cm" % cm,
                 ["%d cm" % x for x in (cm * 10, cm // 10 if cm >= 10 else cm + 1, km)] if cm != km else ["%d cm" % x for x in (cm * 10, cm + 1, cm * 100)],
                 "%d km = %s cm. %s : %s = <b>%d cm</b>." % (km, num(km * 100000), num(km * 100000), num(s_), cm))

    sets = [("Kartor", [(karta, 20)]), ("Ritningar", [(ritning, 20)]), ("Förstoring", [(forstoring, 20)]),
            ("Vilken skala?", [(vilken, 20)]), ("Från verklighet till karta", [(baklanges, 20)])]
    return unit("skala", "F", "Skala: förstoring, förminskning och kartor", "Skala",
                "Skala vid enkel förstoring och förminskning. Proportionella samband vid kartor och ritningar.",
                "Arbetsblad om skala för årskurs %d: kartor, ritningar, förstoring, att bestämma skalan och att räkna från verklighet till karta. 100 uppgifter med facit." % lv,
                "1 : 100 är förminskning", "2 : 1 är förstoring två gånger.", sets,
                ["Skala visar hur mycket en bild är förminskad eller förstorad. Skalan 1 : 100 betyder att 1 cm på bilden är 100 cm i verkligheten.",
                 "Skalan 3 : 1 betyder att bilden är 3 gånger större än verkligheten. Den används för små saker, som insekter.",
                 "På en karta med skalan 1 : 50 000 är 1 cm = 50 000 cm = 500 m i verkligheten."],
                [("Karta 1 : 50 000, 4 cm på kartan", ["4 · 50 000 = 200 000 cm", "200 000 cm = 2 000 m"], "2 km"), ("Skala 5 : 1, myra 6 mm", ["6 · 5"], "30 mm på bilden")],
                [["1 : 100 betyder 100 gånger större", "Det är 100 gånger mindre"], ["Glömmer att göra om cm till m eller km", "100 cm = 1 m, 100 000 cm = 1 km"],
                 ["Skriver skalan baklänges", "Bilden först, verkligheten sedan: bild : verklighet"]],
                [("Vad betyder 1 : 1?", "Att bilden är lika stor som verkligheten."),
                 ("Var används skala?", "På kartor, ritningar av hus, modeller och bilder av små saker."),
                 ("Hur läser man 1 : 25 000?", "Ett till tjugofemtusen. 1 cm på kartan är 250 m i verkligheten.")])


UNITS = {"langd-massa-och-volym": enheter, "tid": tid, "omkrets-och-area": omkrets_area, "vinklar": vinklar,
         "geometriska-figurer-och-kroppar": figurer, "symmetri": symmetri, "koordinatsystem": koordinat, "skala": skala}
